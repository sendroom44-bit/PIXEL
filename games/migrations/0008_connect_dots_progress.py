# Generated for PIXEL: CONNECT
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
    ]
}
