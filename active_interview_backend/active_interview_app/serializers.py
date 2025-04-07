from rest_framework import serializers
from .models import *

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'user', 'uploaded_at']


class PastedTextSerializer(serializers.Serializer):
    text = serializers.CharField()

    class Meta:
        model = PastedText
        fields = ['id', 'user', 'filename', 'content', 'created_at']
        