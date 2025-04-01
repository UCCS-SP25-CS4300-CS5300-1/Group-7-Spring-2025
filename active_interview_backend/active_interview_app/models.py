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
