from django.db import models
<<<<<<< HEAD

class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
=======
from django.contrib.auth.models import User
# Create your models here.
>>>>>>> main
