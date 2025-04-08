import os


from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers

from . import views


# Create router and register views
router = routers.DefaultRouter()


urlpatterns = [
    # Misc. urls
    path('', views.index, name='index'),

    # Auth urls
    path('testlogged/', views.loggedin, name='loggedin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register_page'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # Chat urls
    path('chat/', views.chat_list, name='chat-list'),
    path('chat/create/', views.CreateChat.as_view(), name='chat-create'),
    path('chat/<int:chat_id>/', views.ChatView.as_view(), name='chat-view'),
    path('chat/<int:chat_id>/edit/', views.EditChat.as_view(), name='chat-edit'),
    path('chat/<int:chat_id>/delete/', views.DeleteChat.as_view(), name='chat-delete'),

    # Demo urls
    # path('demo/', views.demo, name='demo'),
    # path('chat-test/', views.test_chat_view, name='chat-test'),

    # api urls
    path('api/', include(router.urls)),

    # Joel's file upload urls
    path('document/', views.DocumentList.as_view(), name='document-list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('api/paste-text/', views.PastedTextView.as_view(), name='save_pasted_text'),
    path('paste-text/<int:pk>/', views.PastedTextDetail.as_view(), name='pasted_text_detail'),
    path('api/files/', views.UploadedFileList.as_view(), name='file_list'),  #List files and uploads.
    path('api/files/<int:pk>/', views.UploadedFileDetail.as_view(), name='file_detail'), #Making changes to files.
    path('pasted-text/', views.PastedTextView.as_view(), name='save_pasted_text'), #For the text box input.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.PROD:
#     # add these urls for production environments only
#     # urlpatterns.append(path('api/', include(router.urls)))
#     pass
# else:
#     # add these urls for non-production environments only
#     # urlpatterns.append(path('api/', include(router.urls)))
#     pass
    
