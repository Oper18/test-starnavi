# coding: utf-8

from rest_framework import serializers

from .models import User, Post, Like, Dislike


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'last_action', 'updated_at', 'date_joined', 'last_login']

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'name', 'description', 'author', 'likes', 'dislikes', 'created_at', 'updated_at']

    def create(self, validated_data):
        instance, status = Post.objects.get_or_create(name=validated_data.get('name'),
                                                      description=validated_data.get('description'),
                                                      author=validated_data.get('user'))
        print(instance, status)
        return instance


class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at', 'updated_at']


class DisikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dislike
        fields = ['id', 'post', 'user', 'created_at', 'updated_at']
