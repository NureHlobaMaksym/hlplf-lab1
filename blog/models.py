from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('Назва', max_length=80, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='categories',
        null=True,
        blank=True,
        verbose_name='Створив',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self) -> str:
        return self.name


class Article(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='articles',
        verbose_name='Категорія',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Автор',
    )
    title = models.CharField('Заголовок', max_length=150)
    body = models.TextField('Текст', validators=[MaxLengthValidator(6000)])
    published_at = models.DateTimeField('Опубліковано', default=timezone.now)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Стаття',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    body = models.TextField('Коментар', validators=[MaxLengthValidator(600)])
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    def __str__(self) -> str:
        return f'{self.author} • {self.article}'
