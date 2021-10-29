from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Song, Genre, Singer
from .models import Voice
from .permissions import IsOwner, IsStaff
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
            permission_classes = [IsStaff]

        return [permission() for permission in permission_classes]

    # GET /voices/me/
    @action(detail=False, methods=["get"])
    def me(self, request):
        user = request.user
        voices = Voice.objects.filter(user_id=user.id).last()
        if not voices:
            raise exceptions.NotFound(detail="Voice 정보가 없습니다.")
        else:
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
        else:
            permission_classes = [IsStaff]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        kwargs["many"] = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET /songs/me/
    @action(detail=False, methods=["get"])
    def me(self, request):
        try:
            user_max_pitch = request.user.voices.last().max_pitch      # 유저와 연결된 voice의 max_pitch
            lower_pitches = find_lower_pitches(user_max_pitch)
            songs = Song.objects.filter(max_pitch__in=lower_pitches)

            if not songs:
                raise exceptions.NotFound(detail="해당 음역대의 노래 정보가 아직 없습니다")

            serializer = SongSerializer(songs, many=True).data
            return Response(serializer)
        except AttributeError:  # 유저의 voice 가 없는 경우
            raise exceptions.NotFound(detail="Voice 정보가 없습니다.")


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.get_queryset().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [IsStaff]


class SingerViewSet(ModelViewSet):
    queryset = Singer.objects.get_queryset().order_by('id')
    serializer_class = SingerSerializer
    permission_classes = [IsStaff]
