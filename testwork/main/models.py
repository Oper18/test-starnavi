# coding: utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    last_action = models.DateTimeField(verbose_name=_('Дата последнего дейтсвия'), null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name=_('Дата изменения'), auto_now=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Post(models.Model):
    name = models.CharField(verbose_name=_('Название поста'), max_length=256, default='No name', blank=True)
    description = models.TextField(verbose_name=_('Текст поста'), null=True, blank=True)
    author = models.ForeignKey(User, verbose_name=_('Автор поста'), on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, through='Like', related_name='like_post')
    dislikes = models.ManyToManyField(User, through='Dislike', related_name='dislike_post')
    created_at = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Дата изменения'), auto_now=True)

    class Meta:
        verbose_name = "Посты"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.name


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return str(self.id)


class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Дизлайк"
        verbose_name_plural = "Дизлайки"

    def __str__(self):
        return str(self.id)
