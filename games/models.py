# -*- coding: utf-8 -*-
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Game(models.Model):
    CATEGORY_CHOICES = [
        ('arcade', 'Аркады'),
        ('sports', 'Спорт'),
        ('logic', 'Логика'),
        ('other', 'Другое'),
    ]
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Адрес игры")
    description = models.TextField(blank=True, verbose_name="Описание на карточке")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name="Категория")
    sort_order = models.PositiveIntegerField(default=100, verbose_name="Порядок в каталоге")
    is_visible = models.BooleanField(default=True, verbose_name="Показывать в каталоге")
    is_enabled = models.BooleanField(default=True, verbose_name="Игра доступна")
    is_new = models.BooleanField(default=False, verbose_name="Показывать NEW")

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Адрес статьи")
    category = models.CharField(max_length=100, default="Новости", verbose_name="Категория")
    description = models.TextField(blank=True, verbose_name="Краткое описание")
    cover = models.ImageField(upload_to="article_covers/", blank=True, null=True, verbose_name="Обложка")
    content = RichTextUploadingField(verbose_name="Текст статьи")
    is_published = models.BooleanField(default=False, verbose_name="Опубликована")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    christmas_mode = models.BooleanField(default=False, verbose_name="Новогоднее настроение")

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Настройки PIXEL"


class PlayerProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='player_profile')
    google_sub = models.CharField(max_length=255, unique=True, verbose_name="Google ID")
    nickname = models.CharField(max_length=32, unique=True, verbose_name="Никнейм")
    avatar_url = models.URLField(max_length=500, blank=True, verbose_name="Аватар Google")
    nickname_changed_at = models.DateTimeField(null=True, blank=True, verbose_name="Последняя смена никнейма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Профиль игрока"
        verbose_name_plural = "Профили игроков"
        ordering = ['-created_at']

    def __str__(self):
        return self.nickname
