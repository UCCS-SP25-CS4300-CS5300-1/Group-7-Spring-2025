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

    class Meta:
        model = UploadedResume
        fields = ["file", "title"]

    def clean_file(self):
        allowed_types = ['txt', 'pdf', 'jpg', 'png']
        uploaded_file = self.cleaned_data.get("file")
        return uploaded_file

