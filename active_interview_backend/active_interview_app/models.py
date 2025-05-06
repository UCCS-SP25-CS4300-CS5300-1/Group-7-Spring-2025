from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UploadedResume(models.Model):  # Renamed from UploadedFile
    # Will be saved under media/uploads/
    file = models.FileField(upload_to='uploads/')
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filesize = models.IntegerField(null=True, blank=True)
    original_filename = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    

    def __str__(self):
        # return f'{self.file.name} uploaded by {self.user}'
        return self.title


# need title for the job listing
class UploadedJobListing(models.Model):  # Renamed from PastedText
    file = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    filepath = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        # return self.filename
        return self.title


class Chat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    difficulty = models.IntegerField(default=5,
                                     validators=[MinValueValidator(1),
                                                 MaxValueValidator(10)])
    messages = models.JSONField()  # Json of the messages object
    key_questions = models.JSONField(default=dict)  # Json of the key questions
    job_listing = models.ForeignKey(UploadedJobListing, null=True,
                                    on_delete=models.SET_NULL)
    resume = models.ForeignKey(UploadedResume, null=True, blank=True,
                               on_delete=models.SET_NULL)

    # interview type
    GENERAL = "GEN"
    SKILLS = "ISK"
    PERSONALITY = "PER"
    FINAL_SCREENING = "FSC"
    INTERVIEW_TYPES = {
        (GENERAL, "General"),
        (SKILLS, "Industry Skills"),
        (PERSONALITY, "Personality/Preliminary"),
        (FINAL_SCREENING, "Final Screening"),
    }
    type = models.CharField(max_length=3, choices=INTERVIEW_TYPES,
                            default=GENERAL)

    # create object itself, not the field
    # all templates for documents in /documents/
    # thing that returns all user files is at views

    modified_date = models.DateTimeField(auto_now=True)  # date last modified

    def __str__(self):
        return self.title
