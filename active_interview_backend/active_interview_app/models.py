from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Chat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    messages = models.JSONField() # Json of the messages object
    # TODO: mandatory foreignkey to job listing object
    # TODO: optional foreignkey to resume object

    modified_date = models.DateTimeField(auto_now=True) # date last modified

    def __str__(self):
        return self.title


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
