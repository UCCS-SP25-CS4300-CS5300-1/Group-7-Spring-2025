from django import forms
from .models import UploadedFile
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


#Defines a Django form for handling file uploads.
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ["file"]

    def clean_file(self):
        allowed_types = ['txt', 'pdf', 'jpg', 'png']
        uploaded_file = self.cleaned_data.get("file")
        #if uploaded_file:
            #Checks for PDF, Word documents, etc.
            #allowed_types = [
            #    "application/pdf",
            #    "application/msword",
            #    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            #]
            #Display error message if incorrect filetype.
            #if uploaded_file.content_type not in allowed_types:
             #   raise forms.ValidationError("Only PDF and Word documents (.doc, .docx) are allowed.")
        return uploaded_file
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

'''

Option 1


    import filetype
    
    def check_file_type(file_path, allowed_types):
        kind = filetype.guess(file_path)
        if kind is None:
            return False
    
        if kind.extension in allowed_types:
             return True
        return False
    
    allowed_types = ['txt', 'pdf', 'jpg', 'png']
    file_path = 'example.pdf'
    if check_file_type(file_path, allowed_types):
        print("File type is allowed.")
    else:
        print("File type is not allowed.")
        
        '''