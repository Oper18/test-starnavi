# coding: utf-8

from django.contrib import admin
from .models import User, Post, Like, Dislike

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')

admin.site.register(Post, PostAdmin)


class LikeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Like, LikeAdmin)


class DislikeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Dislike, DislikeAdmin)
