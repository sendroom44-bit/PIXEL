from django.contrib import admin
from django.urls import path, include
from games.admin_security import admin_otp_verify

admin.site.site_header = "PIXEL CONTROL"
admin.site.site_title = "PIXEL Control"
admin.site.index_title = "Центр управления платформой"

urlpatterns = [
    path('control-room/confirm/', admin_otp_verify, name='pixel_admin_otp'),
    path('control-room/', admin.site.urls),
    path('', include('games.urls')),
]
