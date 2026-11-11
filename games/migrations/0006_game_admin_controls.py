from django.db import migrations, models


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
    ]
