from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Article(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DR', 'Черновик'
        PUBLISHED = 'PB', 'Опубликована'
        ARCHIVED = 'AR', 'Архив'

    title = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Полное название статьи',
        db_index=True,
    )

    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст статьи (ограничений нет)',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        related_query_name='article',
        verbose_name='Автор',
        help_text='Пользователь, который создал статью'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата и время создания статьи (автоматическое устанавливает время)'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
        help_text='Дата и время обновления статьи (автоматическое устанавливает время)'
    )

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус',
        help_text='Статус статьи (черновик (по умолчанию), опубликована, архив)'
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Слаг',
        help_text='URL-название статьи переведённая в транслит'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
