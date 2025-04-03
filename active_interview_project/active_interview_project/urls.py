from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from active_interview_app import views
from django.conf.urls.static import static
from django.conf import settings
#from active_interview_app.views import UploadedFileList, UploadedFileDetail


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),

    # Keep authentication-related URLs from main
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='register_page'),
    path('accounts/logout/', views.logout_view, name='logout'),

    path('testlogged/', views.loggedin, name='loggedin'),
    path('admin/', admin.site.urls),

#    path('api/files/', UploadedFileList.as_view(), name='file_list'),  #List files and uploads.
#    path('api/files/<int:pk>/', UploadedFileDetail.as_view(), name='file_detail'), #Making changes to files.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
