from rest_framework import serializers
from .models import *

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedResume
        fields = ['id', 'file', 'user', 'uploaded_at']


class PastedTextSerializer(serializers.Serializer):
    text = serializers.CharField()

    class Meta:
        model = UploadedJobListing
        fields = ['id', 'user', 'filename', 'content', 'created_at']
        