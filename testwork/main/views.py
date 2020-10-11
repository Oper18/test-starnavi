# coding: utf-8

import datetime

from rest_framework_simplejwt import views as jwt_views

from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import User, Post, Like, Dislike
from .serializers import UserSerializer, PostSerializer, LikesSerializer, DisikesSerializer


class TestTokenObtainPairView(jwt_views.TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super(TestTokenObtainPairView, self).post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data.get('username'))
            user.last_login = datetime.datetime.now()
            user.save()
        return response


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [AllowAny]

        return super(UserViewset, self).get_permissions()

    def list(self, request, *args, **kwargs):
        request.user.last_action = datetime.datetime.now()
        request.user.save()
        return super(UserViewset, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.create(request.data)
        headers = self.get_success_headers(serializer.data)
        return Response(UserSerializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]


    def get_permissions(self):
        if self.action in ['list', 'update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [AllowAny]

        return super(PostViewset, self).get_permissions()

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_action = datetime.datetime.now()
            request.user.save()
            request_data = request.data
            request_data['user'] = request.user
            serializer = self.get_serializer(data=request_data)
            serializer.is_valid()
            instance = serializer.create(request_data)
            return Response(PostSerializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LikeViewset(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_action = datetime.datetime.now()
            request.user.save()
            request_data = request.data
            post = Post.objects.get(pk=request_data.get('post'))
            if request.user != post.author and request.user not in post.likes.all():
                post.likes.add(request.user.id)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_action = datetime.datetime.now()
            request.user.save()
            request_data = request.data
            post = Post.objects.get(pk=request_data.get('post'))
            if request.user != post.author and request.user in post.likes.all():
                post.likes.remove(request.user.id)
        return Response(status=status.HTTP_200_OK)


class DislikeViewset(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_action = datetime.datetime.now()
            request.user.save()
            request_data = request.data
            post = Post.objects.get(pk=request_data.get('post'))
            if request.user not in post.dislikes.all():
                post.dislikes.add(request.user.id)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_action = datetime.datetime.now()
            request.user.save()
            request_data = request.data
            post = Post.objects.get(pk=request_data.get('post'))
            if request.user in post.dislikes.all():
                post.dislikes.remove(request.user.id)
        return Response(status=status.HTTP_200_OK)


class AnaliticView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.last_action = datetime.datetime.now()
            request.user.save()
            date_from = request.query_params.get('date_from', datetime.datetime.now().date())
            date_to = request.query_params.get('date_to', datetime.datetime.now().date() + datetime.timedelta(days=1))

            likes = Like.objects.filter(Q(created_at__gte=date_from) & Q(created_at__lte=date_to))
            dislikes = Dislike.objects.filter(Q(created_at__gte=date_from) & Q(created_at__lte=date_to))

            return Response({'likes': LikesSerializer(likes, many=True).data,
                             'dislikes': DisikesSerializer(dislikes, many=True).data},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class ActivityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'last_login': request.user.last_login,
                             'last_action': request.user.last_action}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
