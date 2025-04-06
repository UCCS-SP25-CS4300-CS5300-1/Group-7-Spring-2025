import os

<<<<<<< HEAD
from django.urls import path, include
from django.contrib.auth import views as auth_views
=======
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import path, include
>>>>>>> d4379a0a7b54aa23f00b0265ba2a6f0d22b46529
from rest_framework import routers

from . import views


# Create router and register views
router = routers.DefaultRouter()


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='login'),
    path('testlogged/', views.loggedin, name='loggedin'),
    path('accounts/', include('django.contrib.auth.urls')),
<<<<<<< HEAD
    path('accounts/register', views.register, name='register_page'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
=======
    path('accounts/register/', views.register, name='register_page'),
    path('accounts/logout/', views.logout_view, name='logout'),
>>>>>>> d4379a0a7b54aa23f00b0265ba2a6f0d22b46529

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

# if settings.PROD:
#     # add these urls for production environments only
#     # urlpatterns.append(path('api/', include(router.urls)))
#     pass
# else:
#     # add these urls for non-production environments only
#     # urlpatterns.append(path('api/', include(router.urls)))
#     pass
    
