from django.contrib import admin
from .models import Game, Article, SiteSettings, PlayerProfile


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sort_order', 'is_visible', 'is_enabled', 'is_new')
    list_editable = ('category', 'sort_order', 'is_visible', 'is_enabled', 'is_new')
    list_filter = ('category', 'is_visible', 'is_enabled', 'is_new')
    search_fields = ('name', 'slug', 'description')
    ordering = ('sort_order', 'name')
    fieldsets = (
        ('Основное', {'fields': ('name', 'slug', 'description', 'category')}),
        ('Публикация и доступ', {'fields': ('sort_order', 'is_visible', 'is_enabled', 'is_new')}),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fieldsets = (('Оформление PIXEL', {'fields': ('christmas_mode',)}),)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'user', 'created_at', 'nickname_changed_at')
    search_fields = ('nickname', 'user__email', 'user__username')
    readonly_fields = ('user', 'google_sub', 'avatar_url', 'created_at', 'nickname_changed_at')
    ordering = ('-created_at',)
