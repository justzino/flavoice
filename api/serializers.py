from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Voice, File, Song, Genre, Singer


class VoiceSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Voice
        fields = ['user', 'max_pitch', 'min_pitch']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        voice = Voice.objects.create(**validated_data, user=request.user)

        return voice


# File upload 를 위한 serializer
class FileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = File
        fields = ['id', 'filename', 'user']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        file = File.objects.create(**validated_data, user=request.user)

        return file


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ['id']


class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'
        read_only_fields = ['id']


class SongSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    singer = SingerSerializer(many=True)

    class Meta:
        model = Song
        fields = ['title', 'max_pitch', 'min_pitch', 'singer', 'genre']
        read_only_fields = ['id']
