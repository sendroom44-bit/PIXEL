
# -*- coding: utf-8 -*-

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    is_visible = models.BooleanField(default=True, verbose_name="Показывать игру")
    is_new = models.BooleanField(default=False, verbose_name="Новинка NEW")

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Адрес статьи")
    category = models.CharField(max_length=100, default="Новости", verbose_name="Категория")
    description = models.TextField(blank=True, verbose_name="Краткое описание")
    cover = models.ImageField(
        upload_to="article_covers/",
        blank=True,
        null=True,
        verbose_name="Обложка"
    )
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
    christmas_mode = models.BooleanField(
        default=False,
        verbose_name="Новогоднее настроение"
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Настройки PIXEL"
