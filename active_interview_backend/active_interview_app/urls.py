import os

from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers

from active_interview_app import views


# Create router and register views
router = routers.DefaultRouter()


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='login'),
    path('testlogged/', views.loggedin, name='loggedin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='register_page'),
    path('accounts/logout/', views.logout_view, name='logout'),
]

# add these urls for non-production environments
if os.environ.get("PROD", "true").lower() == "false":
    urlpatterns.append(path('api/', include(router.urls)))
    
