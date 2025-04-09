from rest_framework import serializers
from .models import *

class UploadedResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedResume
        fields = ['id', 'file', 'user', 'uploaded_at']


class UploadedJobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedJobListing
        fields = ['id', 'user', 'filename', 'content', 'created_at']