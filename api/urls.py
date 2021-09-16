from django.urls import path, include
from rest_framework import routers

from .views import VoiceViewSet, FileViewSet
from .views import SongViewSet, GenreViewSet, SingerViewSet


router = routers.DefaultRouter()
router.register(r'voices', VoiceViewSet)
router.register(r'files', FileViewSet)
router.register(r'songs', SongViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'singers', SingerViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]