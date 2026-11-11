from django.db import migrations, models


def populate_game_settings(apps, schema_editor):
    Game = apps.get_model('games', 'Game')
    category_map = {
        'football': 'sports', 'basketball': 'sports',
        'chess': 'logic', 'mahjong': 'logic', 'tictactoe': 'logic', 'match3': 'logic', 'puzzle': 'logic',
        'paint': 'other', 'city-simulator': 'other', 'chernobyl-fishing': 'other',
    }
    for game in Game.objects.all():
        game.category = category_map.get(game.slug, 'arcade')
        game.sort_order = game.pk * 10
        game.save(update_fields=['category', 'sort_order'])
    Game.objects.get_or_create(
        slug='puzzle',
        defaults={
            'name': 'PIXEL Puzzle',
            'description': 'Собирай изображения, передвигая фрагменты по клеткам.',
            'category': 'logic',
            'sort_order': 5,
            'is_visible': True,
            'is_enabled': True,
            'is_new': True,
        }
    )


class Migration(migrations.Migration):
    dependencies = [('games', '0005_sitesettings')]
    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание на карточке'),
        ),
        migrations.AddField(
            model_name='game',
            name='category',
            field=models.CharField(choices=[('arcade', 'Аркады'), ('sports', 'Спорт'), ('logic', 'Логика'), ('other', 'Другое')], default='other', max_length=20, verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='game',
            name='sort_order',
            field=models.PositiveIntegerField(default=100, verbose_name='Порядок в каталоге'),
        ),
        migrations.AddField(
            model_name='game',
            name='is_enabled',
            field=models.BooleanField(default=True, verbose_name='Игра доступна'),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=models.CharField(max_length=100, unique=True, verbose_name='Адрес игры'),
        ),
        migrations.RunPython(populate_game_settings, migrations.RunPython.noop),
    ]
