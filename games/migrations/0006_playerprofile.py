# Generated for Google-backed PIXEL player profiles.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0005_sitesettings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_sub', models.CharField(max_length=255, unique=True, verbose_name='Google ID')),
                ('nickname', models.CharField(max_length=32, unique=True, verbose_name='Никнейм')),
                ('avatar_url', models.URLField(blank=True, max_length=500, verbose_name='Аватар Google')),
                ('nickname_changed_at', models.DateTimeField(blank=True, null=True, verbose_name='Последняя смена никнейма')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль игрока',
                'verbose_name_plural': 'Профили игроков',
                'ordering': ['-created_at'],
            },
        ),
    ]
