from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Voice
from .serializers import UploadSerializer


# ViewSets define the view behavior.
class VoiceViewSet(ModelViewSet):
    queryset = Voice.objects.all()
    serializer_class = UploadSerializer
