from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Video(models.Model):
    """Модель - видео"""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='videos',
        related_query_name='video',
        verbose_name='Создатель',
        help_text='Создатель видео'
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован',
        help_text='Опубликовано ли видео'
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Название загружаемого видео'
    )

    total_likes = models.PositiveIntegerField(
        default=0,
        verbose_name='Лайки',
        help_text='Количество лайков на видео'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания',
        help_text='Дата и время, когда видео создано'
    )

    def __str__(self):
        return f'{self.name} {self.id}'

    class Meta:
        verbose_name = 'Видеозапись'
        verbose_name_plural = 'Видеозаписи'


class VideoFile(models.Model):
    """Модель - файла видео"""
    video = models.ForeignKey(
        'Video',
        on_delete=models.CASCADE,
        related_name='files',
        related_query_name='file',
        verbose_name='Видео',
        help_text='Ссылка на созданное видео'
    )

    file = models.FileField(
        upload_to='videos/',
        verbose_name='Файл',
        help_text='Загрузка файл'
    )

    class Quality(models.TextChoices):
        HIGH_DEFINITION = 'HD', 'HD'
        FULL_HIGH_DEFINITION = 'FHD', 'FHD'
        ULTRA_HIGH_DEFINITION = 'UHD', 'UHD'

    quality = models.CharField(
        max_length=3,
        choices=Quality.choices,
        default=Quality.HIGH_DEFINITION,
        verbose_name='Качество',
        help_text='Качество видео (HD, FHD, UHD)'
    )

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Видео файл'
        verbose_name_plural = 'Видео файлы'


class Like(models.Model):
    """Модель лайков"""
    video = models.ForeignKey(
        'Video',
        on_delete=models.CASCADE,
        related_name='likes',
        related_query_name='like',
        verbose_name='Лайк',
        help_text='Лайк видео'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        related_query_name='like',
        verbose_name='Пользователь',
        help_text='Пользователь, отправляющий лайк'
    )

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        constraints = [
            models.UniqueConstraint(
                fields=['video', 'user'],
                name='unique_video_user'
            )
        ]
