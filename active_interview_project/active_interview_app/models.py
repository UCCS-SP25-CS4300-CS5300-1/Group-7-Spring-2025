# models.py
from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Will be saved under media/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)
