from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
# False if not in os.environ
DEBUG = env.bool("DEBUG", True)
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, "envs/.env.dev"))

# https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS += env.list("DJANGO_ALLOWED_HOSTS")
THIRD_PARTY_APPS += [
]

# 허용할 Origin 추가
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]

CORS_ORIGIN_ALLOW_ALL = True


# dj-rest-auth 설정: 회원가입 이후 이동할 URL
LOGIN_URL = 'http://localhost:8000/accounts/login'

# Email backend: SMTP 세팅
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')                      # 메일 호스트 서버
EMAIL_HOST_USER = env('EMAIL_HOST_USER')            # 발신할 이메일
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')    # 발신할 메일의 비밀번호
EMAIL_USE_TLS = True                                # TLS 보안 방법
EMAIL_PORT = 587                                    # 통신하는 포트
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Database ------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# DATABASES = {
#     "default": {
#         "ENGINE": env("SQL_ENGINE"),
#         "NAME": env("SQL_DATABASE"),
#         "USER": env("SQL_USER"),
#         "PASSWORD": env("SQL_PASSWORD"),
#         "HOST": env("SQL_HOST"),
#         "PORT": env("SQL_PORT"),
#     }
# }

# Database - venv 용
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}