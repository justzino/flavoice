from django.urls import path, include
from rest_framework import routers
from .views import VoiceViewSet

router = routers.DefaultRouter()
router.register(r'voices', VoiceViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]