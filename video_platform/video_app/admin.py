from django.contrib import admin

from . import models


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    """Регистрация модели Video в админ панель"""

    list_display = ('id', 'owner_info', 'is_published', 'name', 'total_likes', 'created_at')
    list_select_related = ('owner', )
    readonly_fields = ('created_at', 'owner_info_detail')
    search_fields = ('name', 'owner__username')
    ordering = ('-is_published', '-created_at', '-total_likes')

    def owner_info(self, obj):
        """Кастомное поле для удобочитаемости"""

        return f'{obj.owner.username}'
    owner_info.short_description = 'Создатель'

    fieldsets = (
        (
            'Основная информация', {
                'fields': ('name', 'is_published')
            }
        ),
        (
            'Рейтинг и время', {
                'fields': ('total_likes', 'created_at')
            }
        ),
        (
            'Создатель', {
                'fields': ('owner_info_detail', )
            }
        )
    )

    def owner_info_detail(self, obj):
        """Кастомное поле для удобочитаемости"""

        return f'ID: {obj.owner.id}\nUsername: {obj.owner.username}'
    owner_info_detail.short_description = 'Создатель'


@admin.register(models.VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    """Регистрация модели VideoFile в админ панель"""

    list_display = ('video', 'file', 'quality', 'creator')
    list_select_related = ('video', )
    readonly_fields = ('creator', )
    search_fields = ('video__owner__username', 'file')
    ordering = ('quality', )
    fieldsets = (
        (
            'Видео', {
                'fields': ('video', 'file')
            }
        ),
        (
            'Качество', {
                'fields': ('quality', )
            }
        ),
        (
            'Создатель', {
                'fields': ('creator', )
            }
        )
    )

    def creator(self, obj):
        """Кастомное поле для удобочитаемости"""

        return f'{obj.video.owner.username}'
    creator.short_description = 'Создатель'


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    """Регистрация модели Like в админ панель"""

    list_display = ('video', 'user')
    list_select_related = ('video', 'user')
    readonly_fields = ('video', 'user')
    search_fields = ('video__name', 'user__username')
    fieldsets = (
        (
            'Видео', {
                'fields': ('video', )
            }
        ),
        (
            'Создатель', {
                'fields': ('user', )
            }
        )
    )
