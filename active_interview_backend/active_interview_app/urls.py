import os

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers

from . import views


# Create router and register views
router = routers.DefaultRouter()


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='login'),
    path('testlogged/', views.loggedin, name='loggedin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register_page'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # Chat views
    path('chat/', views.chat_list, name='chat-list'),
    path('chat/create/', views.CreateChat.as_view(), name='chat-create'),
    path('chat/<int:chat_id>/', views.ChatView.as_view(), name='chat-view'),
    path('chat/<int:chat_id>/edit/', views.EditChat.as_view(), name='chat-edit'),
    path('chat/<int:chat_id>/delete/', views.DeleteChat.as_view(), name='chat-delete'),

    # Demo view
    path('demo/', views.demo, name='demo'),
    # path('chat-test/', views.test_chat_view, name='chat-test'),

    # api urls
    path('api/', include(router.urls)),
]

if settings.PROD:
    # add these urls for production environments only
    # urlpatterns.append(path('api/', include(router.urls)))
    pass
else:
    # add these urls for non-production environments only
    # urlpatterns.append(path('api/', include(router.urls)))
    pass
    
