from django.forms import ModelForm, ModelChoiceField, IntegerField
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateChatForm(ModelForm):
    difficulty = IntegerField(initial=5, min_value=1, max_value=10)

    listing_choice = ModelChoiceField(
                            queryset=UploadedJobListing.objects.none())
    resume_choice = ModelChoiceField(queryset=UploadedResume.objects.none(),
                                     required=False)

    class Meta:
        model = Chat
        fields = ["title", "type"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # ensure parent object initialized

        if user is not None:
            self.fields['listing_choice'].queryset = \
                UploadedJobListing.objects.filter(user=user)
            self.fields['resume_choice'].queryset = \
                UploadedResume.objects.filter(user=user)


class EditChatForm(ModelForm):
    difficulty = IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Chat
        fields = ["title"]


# Defines a Django form for handling file uploads.
class UploadFileForm(ModelForm):

    # Pretty sure you asked me not to do these, but I forgot and did them.
    # Commented them out just in case you wanted something different.

    # job_listing = forms.ModelChoiceField(
    #   queryset=UploadedJobListing.objects.all(), required=False)
    # resume = forms.ModelChoiceField(
    #   queryset=UploadedResume.objects.all(), required=False)

    class Meta:
        model = UploadedResume
        fields = ["file", "title"]

    def clean_file(self):
        allowed_types = ['txt', 'pdf', 'jpg', 'png']
        uploaded_file = self.cleaned_data.get("file")
        return uploaded_file


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
