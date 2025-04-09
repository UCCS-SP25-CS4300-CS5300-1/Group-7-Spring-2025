from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UploadedResume(models.Model):  # Renamed from UploadedFile
    file = models.FileField(upload_to='uploads/')  # Will be saved under media/uploads/
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filesize = models.IntegerField(null=True, blank=True)
    original_filename = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.file.name} uploaded by {self.user}'


class UploadedJobListing(models.Model):  # Renamed from PastedText
    file = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    filepath = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.filename

class Chat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    messages = models.JSONField() # Json of the messages object
    job_listing = models.ForeignKey(UploadedJobListing, null=True, blank=True, on_delete=models.SET_NULL)
    resume = models.ForeignKey(UploadedResume, null=True, blank=True, on_delete=models.SET_NULL)

    #create object itself, not the field
    #all templates for documents in /documents/
    #thing that returns all user files is at views

    modified_date = models.DateTimeField(auto_now=True) # date last modified

    def __str__(self):
        return self.title



