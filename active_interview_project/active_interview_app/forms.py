from django import forms
from .models import UploadedFile

#Defines a Django form for handling file uploads.
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ["file"]

    def clean_file(self):
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
