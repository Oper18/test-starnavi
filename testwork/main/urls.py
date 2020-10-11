# coding: utf-8

# coding: utf-8

from django.urls import re_path
from rest_framework_simplejwt import views as jwt_views

from.views import UserViewset, PostViewset, LikeViewset, DislikeViewset, AnaliticView, ActivityView, \
    TestTokenObtainPairView

urlpatterns = [
    re_path(r'^api/token/$', TestTokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/token/refresh/', TestTokenObtainPairView.as_view(), name='token_refresh'),
    re_path(r'^api/account/$', UserViewset.as_view({
        'put': 'create',
    })),
    re_path(r'^api/account/(?P<pk>\d+)/$', UserViewset.as_view({
        'get': 'list',
    })),
    re_path(r'^api/post/$', PostViewset.as_view({
        'get': 'list',
        'put': 'create',
    })),
    re_path(r'^api/post/(?P<pk>\d+)/$', PostViewset.as_view({
        'post': 'update',
        'delete': 'destroy',
    })),
    re_path(r'^api/like/$', LikeViewset.as_view()),
    re_path(r'^api/dislike/$', DislikeViewset.as_view()),
    re_path(r'^api/analitic/$', AnaliticView.as_view()),
    re_path(r'^api/activity/$', ActivityView.as_view()),
]