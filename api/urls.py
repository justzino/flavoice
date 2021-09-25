from django.urls import path, include
from rest_framework import routers

from .views import VoiceViewSet
from .views import SongViewSet, GenreViewSet, SingerViewSet


router = routers.DefaultRouter()
router.register('voices', VoiceViewSet)
router.register('songs', SongViewSet)
router.register('genres', GenreViewSet)
router.register('singers', SingerViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]