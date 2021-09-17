from rest_framework.viewsets import ModelViewSet

from .models import Song, Genre, Singer
from .models import Voice, File
from .serializers import FileSerializer
from .serializers import GenreSerializer
from .serializers import SingerSerializer
from .serializers import SongSerializer
from .serializers import VoiceSerializer


class VoiceViewSet(ModelViewSet):
    queryset = Voice.objects.all()
    serializer_class = VoiceSerializer


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class SingerViewSet(ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
