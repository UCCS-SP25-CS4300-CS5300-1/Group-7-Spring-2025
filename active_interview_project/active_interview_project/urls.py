from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from active_interview_app import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
<<<<<<< HEAD
=======
    path('', views.index, name='index'),
    path('', views.index, name = 'login'),
    path('testlogged/', views.loggedin, name ='loggedin'),
     path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name = 'register_page'),
    path('accounts/logout/', views.logout_view, name='logout'),
>>>>>>> main
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)