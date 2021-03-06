from json.decoder import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from accounts.models import CustomUser as User

BASE_URL = 'https://flavoice.shop/'
# BASE_URL = 'http://localhost:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'
REST_API_KEY = settings.KAKAO_REST_API_KEY


def kakao_login(request):

    """
    이 함수와 매핑된 url로 들어가면, client_id, redirect uri 등과 같은 정보를 url parameter로 함께 보내 리다이렉트한다.
    그러면 구글 로그인 창이 뜨고, 알맞은 아이디, 비밀번호로 진행하면 Callback URI로 Code값이 들어가게 된다.
    """

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI

    # Access Token Request
    """
    Google API Server에 응답받은 Code, client_secret, state와 같은 url parameter를 함께 Post 요청을 보낸다.
    문제없이 성공하면, access_token을 가져올 수 있다.
    """
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")

    # print(f"access_token: {access_token}")

    # Email Request
    """
    응답받은 Access Token을 로그인된 사용자의 Email을 응답받기 위해 url parameter에 포함하여 요청.
    Access Token이 틀렸거나, 에러 발생으로 200 OK 코드를 응답받지 못하면 400으로 Response
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    profile_json = profile_request.json()
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    kakao_account = profile_json.get('kakao_account')

    """
    kakao_account에서 이메일 외에 카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 로 확인 가능
    """
    # print(f"kakao_account: {kakao_account}")
    email = kakao_account.get('email')
    # print(f"email: {email}")

    # Signup or Signin Request
    """
    1. 전달받은 email과 동일한 Email이 있는지 찾아본다.
    2-1. 만약 있다면?
           - FK로 연결되어있는 social account 테이블에서 이메일의 유저가 있는지 체크
           - 없으면 일반 계정이므로, 에러 메세지와 함께 400 리턴
           - 있지만 다른 Provider로 가입되어 있으면 에러 메세지와 함께 400 리턴
           - 위 두개에 걸리지 않으면 로그인 진행, 해당 유저의 JWT 발급, 그러나 도중에
             예기치 못한 오류가 발생하면 에러 메세지와 함께 오류 Status 응답
    2-2. 없다면 (신규 유저이면)
           - 회원가입 진행 및 해당 유저의 JWT 발급
           - 그러나 도중에 예기치 못한 오류가 발생하면 에러 메세지와 함께 오류 Status응답
    """

    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST
            )
        if social_user.provider != 'kakao':
            return JsonResponse(
                {'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST
            )

        # 기존에 Kakao로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        # print(data)
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
