import time
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.crypto import salted_hmac
from .models import Game


ADMIN_PREFIX = '/control-room/'
VERIFY_PATH = '/control-room/confirm/'


def _otp_digest(code):
    return salted_hmac('pixel-admin-email-otp', code, secret=settings.SECRET_KEY).hexdigest()


def issue_admin_code(request):
    now = int(time.time())
    if request.session.get('pixel_otp_sent_at', 0) > now - 60:
        return
    if not settings.DEBUG and not settings.EMAIL_HOST:
        request.session['pixel_otp_error'] = 'Почтовая отправка не настроена. Администратор должен добавить SMTP-переменные в Render.'
        return
    import secrets
    code = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    send_mail(
        'Код входа в PIXEL CONTROL',
        'Код подтверждения: %s\nОн действует 5 минут. Никому не сообщайте этот код.' % code,
        settings.DEFAULT_FROM_EMAIL,
        [settings.PIXEL_ADMIN_EMAIL],
        fail_silently=False,
    )
    request.session['pixel_otp_hash'] = _otp_digest(code)
    request.session['pixel_otp_expires'] = now + 300
    request.session['pixel_otp_sent_at'] = now
    request.session['pixel_otp_attempts'] = 0
    request.session.pop('pixel_otp_error', None)


class AdminSecondFactorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith(ADMIN_PREFIX) and path != VERIFY_PATH and not path.startswith('/control-room/logout/'):
            user = getattr(request, 'user', None)
            if user and user.is_authenticated and user.is_staff:
                verified_at = request.session.get('pixel_admin_verified_at')
                now = int(time.time())
                if verified_at and now - int(verified_at) <= 1800:
                    pass
                else:
                    request.session.pop('pixel_admin_verified_at', None)
                    if not request.session.get('pixel_otp_hash') or now > request.session.get('pixel_otp_expires', 0):
                        try:
                            issue_admin_code(request)
                        except Exception:
                            request.session['pixel_otp_error'] = 'Не удалось отправить письмо. Проверьте SMTP-настройки.'
                    return redirect('pixel_admin_otp')
        return self.get_response(request)


class GameAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and not request.path.startswith(('/control-room/', '/admin/', '/articles/')):
            segment = request.path.strip('/').split('/')[0]
            if segment:
                game = Game.objects.filter(slug=segment).only('is_enabled').first()
                if game and not game.is_enabled:
                    from django.http import HttpResponse
                    return HttpResponse('Эта игра временно отключена администрацией PIXEL.', status=403)
        return self.get_response(request)
