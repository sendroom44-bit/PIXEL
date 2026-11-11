from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def add_tanks_to_catalog(apps, schema_editor):
    Game = apps.get_model('games', 'Game')
    Game.objects.get_or_create(
        slug='tanks',
        defaults={
            'name': 'PIXEL Tanks',
            'description': 'Аркадные танковые бои: против ботов или онлайн с игроками.',
            'category': 'arcade',
            'sort_order': 15,
            'is_visible': True,
            'is_enabled': True,
            'is_new': True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0006_playerprofile'),
        ('games', '0006_game_admin_controls'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TankRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=12, unique=True)),
                ('state', models.JSONField(default=dict)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tank_rooms', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-updated_at']},
        ),
        migrations.RunPython(add_tanks_to_catalog, migrations.RunPython.noop),
    ]
