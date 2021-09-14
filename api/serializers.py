from rest_framework import serializers

from .models import User, Voice, File, Song, Genre, Singer

# Serializers define the API representation.
class UploadSerializer(serializers.ModelSerializer):

class UserSerializer(serializers.ModelSerializer):
    # password 를 serializer 로 보여주는 것 방지
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "phone_number",
            "birthday",
            "password",  # password 입력 받기 위해
        )

        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

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
