from django.urls import path, include
from rest_framework import routers

from .views import kakao_login, kakao_callback, KakaoLogin


router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),

    path('kakao/login/', kakao_login, name='kakao_login'),
    path('kakao/callback/', kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
]