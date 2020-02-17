from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from .views import MovieData,UserData,RateData,CommentData

urlpatterns = [
    url(r'^movie$',MovieData.as_view()),
    url(r'^movie/(?P<name>\w+)/$', MovieData.as_view()),
    url(r'^user/(?P<id>\w+)/$',UserData.as_view()),
    url(r'^rate/$',RateData.as_view()),
    url(r'^comment/$',CommentData.as_view())
]
