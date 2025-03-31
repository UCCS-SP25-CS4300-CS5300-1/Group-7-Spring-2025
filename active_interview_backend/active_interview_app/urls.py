import os

from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers

from . import views


# Create router and register views
router = routers.DefaultRouter()


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='login'),
    path('chat/', views.chat, name='chat'),
    path('testlogged/', views.loggedin, name='loggedin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='register_page'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # Demo view
    path('demo/', views.demo, name='demo'),
    # path('chat-test/', views.test_chat_view, name='chat-test'),

    # api urls
    path('api/', include(router.urls)),
]

if os.environ.get("PROD", "true").lower() == "true":
    # add these urls for production environments only
    # urlpatterns.append(path('api/', include(router.urls)))
    pass
else:
    # add these urls for non-production environments only
    # urlpatterns.append(path('api/', include(router.urls)))
    pass
    
