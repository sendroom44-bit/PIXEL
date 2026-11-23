# Generated for PIXEL: CONNECT
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def add_connect_dots_to_catalog(apps, schema_editor):
    Game = apps.get_model('games', 'Game')
    Game.objects.get_or_create(
        slug='connect-dots',
        defaults={
            'name': 'PIXEL: CONNECT',
            'description': '150 уровней: соединяй точки по порядку, открывай рисунки и собирай звёзды.',
            'category': 'logic',
            'sort_order': 60,
            'is_visible': True,
            'is_enabled': True,
            'is_new': True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0007_tankroom'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectDotsProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('energy', models.PositiveSmallIntegerField(default=5, verbose_name='Энергия')),
                ('energy_updated_at', models.DateTimeField(auto_now_add=True)),
                ('unlocked_level', models.PositiveSmallIntegerField(default=1)),
                ('completed_levels', models.JSONField(blank=True, default=list)),
                ('total_stars', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='connect_dots_progress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Прогресс PIXEL: CONNECT',
                'verbose_name_plural': 'Прогресс PIXEL: CONNECT',
            },
        ),
        migrations.RunPython(add_connect_dots_to_catalog, migrations.RunPython.noop),
    ]
}
