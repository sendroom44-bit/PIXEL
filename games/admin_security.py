import time
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils.crypto import salted_hmac
from .middleware import issue_admin_code


@staff_member_required(login_url='/control-room/login/')
def admin_otp_verify(request):
    now = int(time.time())
    error = request.session.pop('pixel_otp_error', '')

    if request.method == 'POST' and request.POST.get('resend') == '1':
        sent_at = int(request.session.get('pixel_otp_sent_at', 0))
        if now - sent_at < 60:
            error = 'Повторный код можно запросить не чаще одного раза в минуту.'
        else:
            request.session.pop('pixel_otp_hash', None)
            request.session.pop('pixel_otp_sent_at', None)
            try:
                issue_admin_code(request)
                error = request.session.get('pixel_otp_error', 'Новый код отправлен. Проверьте почту.')
            except Exception:
                error = 'Не удалось отправить письмо. Проверьте настройки почты.'

    elif request.method == 'POST':
        attempts = int(request.session.get('pixel_otp_attempts', 0))
        if attempts >= 5:
            request.session.pop('pixel_otp_hash', None)
            error = 'Слишком много попыток. Запросите новый код.'
        elif now > int(request.session.get('pixel_otp_expires', 0)):
            error = 'Срок действия кода истёк. Запросите новый.'
        else:
            code = ''.join(ch for ch in request.POST.get('code', '') if ch.isdigit())
            expected = request.session.get('pixel_otp_hash', '')
            digest = salted_hmac('pixel-admin-email-otp', code, secret=settings.SECRET_KEY).hexdigest()
            if len(code) == 6 and expected and digest == expected:
                request.session['pixel_admin_verified_at'] = now
                for key in ('pixel_otp_hash', 'pixel_otp_expires', 'pixel_otp_attempts', 'pixel_otp_sent_at'):
                    request.session.pop(key, None)
                return redirect('/control-room/')
            request.session['pixel_otp_attempts'] = attempts + 1
            error = 'Неверный код. Проверьте письмо и попробуйте ещё раз.'

    return render(request, 'admin/pixel_otp.html', {
        'email': settings.PIXEL_ADMIN_EMAIL,
        'error': error,
        'sent': bool(request.session.get('pixel_otp_hash')),
    })
