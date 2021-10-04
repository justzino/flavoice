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


class SongViewSet(ModelViewSet):
    queryset = Song.objects.get_queryset().order_by('max_pitch')
    serializer_class = SongSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.get_queryset().order_by('id')
    serializer_class = GenreSerializer


class SingerViewSet(ModelViewSet):
    queryset = Singer.objects.get_queryset().order_by('id')
    serializer_class = SingerSerializer
