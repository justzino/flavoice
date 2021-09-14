from django.urls import path, include
from rest_framework import routers

from .views import SongViewSet, UsersView, MeView, user_detail, login

router = routers.DefaultRouter()
router.register(r'voices', VoiceViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
    path("users/", UsersView.as_view()),
    path("users/me/", MeView.as_view()),
    path("users/<int:pk>/", user_detail),
    path("users/login/", login),
]