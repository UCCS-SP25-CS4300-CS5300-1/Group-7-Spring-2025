"""
URL configuration for active_interview_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from active_interview_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name = 'login'),
    path('testlogged/', views.loggedin, name ='loggedin'),
     path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name = 'register_page'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
]
