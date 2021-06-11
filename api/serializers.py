from rest_framework import serializers
from .models import Voice


# Serializers define the API representation.
class UploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voice
        fields = ['file', ]

    def create(self, validated_data):
        voice = super().create(validated_data)
        voice.save()

        return voice


# Serializer for multiple files upload.
class MultipleFilesUploadSerializer(serializers.ModelSerializer):
    file_uploaded = serializers.ListField(serializers.FileField())

    class Meta:
        model = Voice
        fields = ['file', 'description', ]
