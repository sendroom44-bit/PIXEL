from .models import SiteSettings


def site_settings(request):
    settings = SiteSettings.objects.first()

    return {
        'site_settings': settings,
        'christmas_mode': settings.christmas_mode if settings else False,
    }