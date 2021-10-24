from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Song, Genre, Singer
from .models import Voice
from .permissions import IsOwner
from .serializers import GenreSerializer
from .serializers import SingerSerializer
from .serializers import SongSerializer
from .serializers import VoiceSerializer


class VoiceViewSet(ModelViewSet):

    queryset = Voice.objects.all()
    serializer_class = VoiceSerializer
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # (POST /voices/)
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        # (GET /voices/me/) or (PUT /voices/1/)
        elif self.action == "me" or self.action == "update":
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    # GET /voices/me/
    @action(detail=False, methods=["get"])
    def me(self, request):
        user = request.user
        voices = Voice.objects.filter(user_id=user.id)
        serializer = VoiceSerializer(voices, many=True).data
        return Response(serializer)


# class FileViewSet(ModelViewSet):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer


# 해당 pitch 보다 작거나 같은 5개 pitch list return
def find_lower_pitches(pitch: str):
    pitch_list = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note, octave = '', ''
    if pitch[1] == '#':
        note, octave = pitch[:2], int(pitch[2:])     # 'F#', 5
    else:
        note, octave = pitch[:1], int(pitch[1:])

    idx = pitch_list.index(note)
    lower_pitches = []
    for i in range(5):
        lower_pitches.append(pitch_list[idx] + str(octave))

        idx -= 1
        if idx < 0:
            idx += 12
            octave -= 1
    return lower_pitches


class SongViewSet(ModelViewSet):
    queryset = Song.objects.get_queryset().order_by('max_pitch')
    serializer_class = SongSerializer

    def get_permissions(self):
        # (GET /songs/me/)
        if self.action == "me":
            permission_classes = [IsOwner]
        # (POST /songs/) (DELETE /songs/{id}/) (PUT /songs/{id}/) (PATCH /songs/{id}/)
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    # GET /songs/me/
    @action(detail=False, methods=["get"])
    def me(self, request):
        user_max_pitch = request.user.voices.all()[0].max_pitch
        lower_pitches = find_lower_pitches(user_max_pitch)
        songs = Song.objects.filter(max_pitch__in=lower_pitches)
        serializer = SongSerializer(songs, many=True).data
        return Response(serializer)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.get_queryset().order_by('id')
    serializer_class = GenreSerializer


class SingerViewSet(ModelViewSet):
    queryset = Singer.objects.get_queryset().order_by('id')
    serializer_class = SingerSerializer
