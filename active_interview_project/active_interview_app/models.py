# models.py
from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Will be saved under media/uploads/
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filesize = models.IntegerField(null=True, blank=True)
    original_filename = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.file.name} uploaded by {self.user}'

class PastedText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename