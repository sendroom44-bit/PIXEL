import hmac
import json
import secrets
import time
from datetime import timedelta
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required

from .models import Game, Article, PlayerProfile, TankRoom


def home(request):
    games = Game.objects.filter(is_visible=True, is_enabled=True).order_by('sort_order', 'name')
    return render(request, 'games/home.html', {'games': games})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('account')
    return render(request, 'games/login.html')


def google_login(request):
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        messages.error(request, 'Вход через Google пока не настроен. Администратору нужно добавить OAuth-ключи в Render.')
        return redirect('login')
    state = secrets.token_urlsafe(32)
    request.session['google_oauth_state'] = state
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'prompt': 'select_account',
    }
    return redirect('https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params))


def google_callback(request):
    error = request.GET.get('error')
    if error:
        messages.error(request, 'Вход через Google отменён или не выполнен.')
        return redirect('login')

    returned_state = request.GET.get('state', '')
    saved_state = request.session.pop('google_oauth_state', '')
    if not saved_state or not hmac.compare_digest(saved_state, returned_state):
        return HttpResponseBadRequest('Проверка безопасности не пройдена. Вернитесь на страницу входа и попробуйте снова.')

    code = request.GET.get('code')
    if not code:
        messages.error(request, 'Google не вернул код авторизации. Попробуйте ещё раз.')
        return redirect('login')

    token_payload = urlencode({
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }).encode('utf-8')
    try:
        token_request = Request(
            'https://oauth2.googleapis.com/token',
            data=token_payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            method='POST',
        )
        with urlopen(token_request, timeout=12) as response:
            token_data = json.loads(response.read().decode('utf-8'))
        access_token = token_data.get('access_token')
        if not access_token:
            raise ValueError('Google не выдал access token')

        userinfo_request = Request(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': 'Bearer ' + access_token},
        )
        with urlopen(userinfo_request, timeout=12) as response:
            google_data = json.loads(response.read().decode('utf-8'))
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError):
        messages.error(request, 'Не удалось подтвердить аккаунт Google. Попробуйте войти ещё раз.')
        return redirect('login')

    google_sub = str(google_data.get('sub', '')).strip()
    email = str(google_data.get('email', '')).strip().lower()
    verified = google_data.get('email_verified') is True or str(google_data.get('email_verified', '')).lower() == 'true'
    if not google_sub or not email or not verified:
        messages.error(request, 'Google не подтвердил адрес почты. Используйте подтверждённый Google-аккаунт.')
        return redirect('login')

    profile = PlayerProfile.objects.select_related('user').filter(google_sub=google_sub).first()
    if profile:
        user = profile.user
        profile.avatar_url = google_data.get('picture', '')[:500]
        profile.save(update_fields=['avatar_url'])
        if user.email != email:
            user.email = email
            user.save(update_fields=['email'])
    else:
        base_username = 'google_' + google_sub
        username = base_username[:150]
        user = User.objects.filter(username=username).first()
        if user is None:
            user = User(username=username, email=email, first_name=str(google_data.get('given_name', ''))[:150])
            user.set_unusable_password()
            user.save()
        display_name = str(google_data.get('name') or google_data.get('given_name') or 'Игрок PIXEL').strip()
        nickname = _unique_nickname(display_name)
        profile = PlayerProfile.objects.create(
            user=user,
            google_sub=google_sub,
            nickname=nickname,
            avatar_url=str(google_data.get('picture', ''))[:500],
        )

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    request.session.pop('google_oauth_state', None)
    return redirect('account')


def _unique_nickname(value, exclude_profile_id=None):
    cleaned = ''.join(ch for ch in value if ch.isalnum() or ch in ' _-').strip()
    cleaned = ' '.join(cleaned.split())[:32] or 'Игрок'
    candidate = cleaned
    number = 1
    while PlayerProfile.objects.filter(nickname__iexact=candidate).exclude(pk=exclude_profile_id).exists():
        suffix = ' (' + str(number) + ')'
        candidate = cleaned[:32 - len(suffix)] + suffix
        number += 1
    return candidate


@login_required(login_url='login')
def account(request):
    profile, created = PlayerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'google_sub': 'legacy_' + str(request.user.pk),
            'nickname': _unique_nickname(request.user.first_name or request.user.username),
        },
    )
    if request.method == 'POST':
        requested_nickname = request.POST.get('nickname', '').strip()
        if profile.nickname_changed_at and timezone.now() < profile.nickname_changed_at + timedelta(hours=48):
            available_at = profile.nickname_changed_at + timedelta(hours=48)
            messages.error(request, 'Никнейм можно будет изменить ' + timezone.localtime(available_at).strftime('%d.%m.%Y в %H:%M') + '.')
        elif not requested_nickname:
            messages.error(request, 'Введи новый никнейм.')
        elif len(requested_nickname) > 32:
            messages.error(request, 'Никнейм должен быть не длиннее 32 символов.')
        else:
            new_nickname = _unique_nickname(requested_nickname, profile.pk)
            if new_nickname == profile.nickname:
                messages.info(request, 'Этот никнейм уже установлен.')
            else:
                profile.nickname = new_nickname
                profile.nickname_changed_at = timezone.now()
                profile.save(update_fields=['nickname', 'nickname_changed_at'])
                messages.success(request, 'Никнейм обновлён: ' + new_nickname)
        return redirect('account')
    return render(request, 'games/account.html', {'profile': profile})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


def mahjong(request):
    return render(request, 'games/mahjong.html')


def football(request):
    return render(request, 'games/football.html')


def basketball(request):
    return render(request, 'games/basketball.html')


def tictactoe(request):
    return render(request, 'games/tictactoe.html')


def simpsons(request):
    return render(request, 'games/simpsons.html')


def chess(request):
    return render(request, 'games/chess.html')


def breakout(request):
    return render(request, 'games/breakout.html')


def prison_pacman(request):
    return render(request, 'games/prison_pacman.html')


def prison_pacman2(request):
    return render(request, 'games/prison_pacman2.html')


def paint(request):
    return render(request, 'games/paint.html')


def city_simulator(request):
    return render(request, 'games/city_simulator.html')


def christmas_tower(request):
    return render(request, 'games/christmas_tower.html')


def santa_delivery(request):
    return render(request, 'games/santa_delivery.html')


def match3(request):
    return render(request, 'games/match3.html')


def chernobyl_fishing(request):
    return render(request, 'games/chernobyl_fishing.html')


def christmas_circuit(request):
    return render(request, 'games/christmas_circuit.html')


def puzzle(request):
    return render(request, 'games/puzzle.html')


def articles(request):
    articles_list = Article.objects.filter(is_published=True)
    return render(request, 'games/articles.html', {'articles': articles_list})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'games/article_detail.html', {'article': article})


# PIXEL Tanks: room state is stored in the database so players can meet across devices.
def tanks(request):
    return render(request, 'games/tanks.html')


def _tank_player_name(user):
    try:
        return user.player_profile.nickname
    except PlayerProfile.DoesNotExist:
        return user.first_name or user.username


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def tanks_rooms(request):
    if request.method == 'GET':
        now = timezone.now()
        rooms = TankRoom.objects.filter(is_active=True, updated_at__gte=now - timedelta(minutes=3)).order_by('-updated_at')[:30]
        return JsonResponse({'rooms': [
            {'code': room.code, 'players': len(room.state.get('players', [])),
             'host': room.state.get('players', [{}])[0].get('name', 'Игрок'),
             'teams': [p.get('team') for p in room.state.get('players', [])]}
            for room in rooms
        ]})
    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error': 'Некорректный запрос'}, status=400)
    team = data.get('team')
    if team not in ('ussr', 'germany'):
        return JsonResponse({'error': 'Выбери команду'}, status=400)
    code = get_random_string(6, allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    player = {'id': request.user.pk, 'name': _tank_player_name(request.user)[:32],
              'team': team, 'x': 80 if team == 'ussr' else 560, 'y': 80, 'angle': 0, 'hp': 3}
    room = TankRoom.objects.create(code=code, host=request.user, state={'players': [player], 'bullets': [], 'map': 1})
    return JsonResponse({'ok': True, 'code': room.code, 'state': room.state})


@login_required(login_url='login')
@require_POST
def tanks_join(request, code):
    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error': 'Некорректный запрос'}, status=400)
    team = data.get('team')
    if team not in ('ussr', 'germany'):
        return JsonResponse({'error': 'Выбери команду'}, status=400)
    with transaction.atomic():
        room = TankRoom.objects.select_for_update().filter(code=code.upper(), is_active=True).first()
        if not room:
            return JsonResponse({'error': 'Комната не найдена'}, status=404)
        players = room.state.get('players', [])
        existing = next((p for p in players if p.get('id') == request.user.pk), None)
        if not existing and len(players) >= 2:
            return JsonResponse({'error': 'Комната уже заполнена'}, status=409)
        if existing:
            existing['team'] = team
        else:
            players.append({'id': request.user.pk, 'name': _tank_player_name(request.user)[:32],
                            'team': team, 'x': 80 if team == 'ussr' else 560, 'y': 400, 'angle': 0, 'hp': 3})
        room.state['players'] = players
        room.save(update_fields=['state', 'updated_at'])
    return JsonResponse({'ok': True, 'code': room.code, 'state': room.state})


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def tanks_room_state(request, code):
    room = TankRoom.objects.filter(code=code.upper(), is_active=True).first()
    if not room:
        return JsonResponse({'error': 'Комната не найдена'}, status=404)
    players = room.state.get('players', [])
    me = next((p for p in players if p.get('id') == request.user.pk), None)
    if not me:
        return JsonResponse({'error': 'Ты не участник этой комнаты'}, status=403)
    if request.method == 'GET':
        return JsonResponse({'state': room.state, 'me': request.user.pk})
    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error': 'Некорректный запрос'}, status=400)
    me['x'] = max(28, min(612, int(data.get('x', me.get('x', 80)))))
    me['y'] = max(28, min(452, int(data.get('y', me.get('y', 80)))))
    me['angle'] = int(data.get('angle', me.get('angle', 0))) % 360
    now = timezone.now().timestamp()
    bullets = []
    for bullet in room.state.get('bullets', []):
        elapsed = min(0.5, max(0, now - bullet.get('t', now)))
        angle = bullet.get('angle', 0) * 3.141592653589793 / 180
        bullet['x'] += __import__('math').cos(angle) * 5 * elapsed * 60
        bullet['y'] += __import__('math').sin(angle) * 5 * elapsed * 60
        bullet['t'] = now
        hit = False
        if bullet['x'] < 0 or bullet['x'] > 640 or bullet['y'] < 0 or bullet['y'] > 480:
            hit = True
        for target in players:
            if target.get('id') != bullet.get('owner') and target.get('team') != bullet.get('team') and target.get('hp', 3) > 0:
                if (target['x'] - bullet['x']) ** 2 + (target['y'] - bullet['y']) ** 2 < 18 ** 2:
                    target['hp'] = max(0, target.get('hp', 3) - 1)
                    hit = True
        if not hit:
            bullets.append(bullet)
    if data.get('fire'):
        bullets.append({'x': me['x'], 'y': me['y'], 'angle': me['angle'],
                        'team': me['team'], 'owner': request.user.pk, 't': now})
    room.state['bullets'] = bullets[-30:]
    room.state['players'] = players
    room.save(update_fields=['state', 'updated_at'])
    return JsonResponse({'ok': True})


@login_required(login_url='login')
@require_POST
def tanks_leave(request, code):
    room = TankRoom.objects.filter(code=code.upper(), is_active=True).first()
    if not room:
        return JsonResponse({'ok': True})
    room.state['players'] = [p for p in room.state.get('players', []) if p.get('id') != request.user.pk]
    if not room.state['players']:
        room.is_active = False
        room.save(update_fields=['state', 'is_active', 'updated_at'])
    else:
        room.save(update_fields=['state', 'updated_at'])
    return JsonResponse({'ok': True})
