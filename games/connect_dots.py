import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import ConnectDotsProgress

MAX_ENERGY = 5
ENERGY_INTERVAL = timedelta(minutes=5)
MAX_LEVEL = 150


def _refresh_energy(progress):
    now = timezone.now()
    if progress.energy >= MAX_ENERGY:
        progress.energy = MAX_ENERGY
        progress.energy_updated_at = now
        return
    elapsed = now - progress.energy_updated_at
    recovered = int(elapsed.total_seconds() // ENERGY_INTERVAL.total_seconds())
    if recovered:
        progress.energy = min(MAX_ENERGY, progress.energy + recovered)
        progress.energy_updated_at += ENERGY_INTERVAL * recovered
        if progress.energy >= MAX_ENERGY:
            progress.energy_updated_at = now


def _state(progress):
    _refresh_energy(progress)
    progress.save(update_fields=['energy', 'energy_updated_at'])
    wait = 0
    if progress.energy < MAX_ENERGY:
        elapsed = (timezone.now() - progress.energy_updated_at).total_seconds()
        wait = max(0, int(ENERGY_INTERVAL.total_seconds() - elapsed))
    return {
        'energy': progress.energy,
        'max_energy': MAX_ENERGY,
        'wait_seconds': wait,
        'unlocked_level': progress.unlocked_level,
        'completed_levels': progress.completed_levels,
        'total_stars': progress.total_stars,
        'max_level': MAX_LEVEL,
    }


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def connect_dots_api(request):
    with transaction.atomic():
        progress, unused = ConnectDotsProgress.objects.select_for_update().get_or_create(user=request.user)
        _refresh_energy(progress)

        if request.method == 'GET':
            progress.save(update_fields=['energy', 'energy_updated_at'])
            return JsonResponse(_state(progress))

        try:
            data = json.loads(request.body.decode('utf-8') or '{}')
        except (ValueError, UnicodeDecodeError):
            return JsonResponse({'error': 'Некорректный запрос'}, status=400)

        action = data.get('action')
        try:
            level = int(data.get('level', 1))
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Некорректный уровень'}, status=400)

        if level < 1 or level > MAX_LEVEL:
            return JsonResponse({'error': 'Такого уровня нет'}, status=400)
        if level > progress.unlocked_level:
            return JsonResponse({'error': 'Сначала пройди предыдущий уровень'}, status=403)

        if action in ('mistake', 'replay'):
            if action == 'replay' and level not in progress.completed_levels:
                return JsonResponse({'error': 'Повторно можно запускать только пройденный уровень'}, status=400)
            if progress.energy <= 0:
                progress.save(update_fields=['energy', 'energy_updated_at'])
                return JsonResponse({'error': 'Энергия закончилась', 'state': _state(progress)}, status=429)
            progress.energy -= 1
            if progress.energy == 0:
                progress.energy_updated_at = timezone.now()
            elif progress.energy >= MAX_ENERGY:
                progress.energy_updated_at = timezone.now()
            progress.save(update_fields=['energy', 'energy_updated_at'])
            return JsonResponse({'ok': True, 'state': _state(progress)})

        if action == 'complete':
            if level not in progress.completed_levels:
                progress.completed_levels = sorted(progress.completed_levels + [level])
                stars = max(1, min(3, int(data.get('stars', 1))))
                progress.total_stars += stars
                if level == progress.unlocked_level and level < MAX_LEVEL:
                    progress.unlocked_level += 1
                progress.save(update_fields=['completed_levels', 'total_stars', 'unlocked_level', 'energy', 'energy_updated_at'])
            return JsonResponse({'ok': True, 'state': _state(progress)})

        return JsonResponse({'error': 'Неизвестное действие'}, status=400)



@login_required(login_url='login')
def connect_dots_page(request):
    return render(request, 'games/connect_dots.html')
