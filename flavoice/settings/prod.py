from .base import *  # noqa

DEBUG = True
env.read_env(os.path.join(BASE_DIR, "envs/.env.prod"))

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
THIRD_PARTY_APPS += [
]

# 허용할 Origin 추가
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]

CORS_ORIGIN_ALLOW_ALL = True        # 임시로 다 열어둠

# dj-rest-auth 설정: 회원가입 이후 이동할 URL
LOGIN_URL = 'https://flavoice.shop/accounts/login'

# Email backend: SMTP 세팅
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
SERVER_EMAIL = env('EMAIL_HOST_USER')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Database ------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": env("SQL_ENGINE"),
        "NAME": env("SQL_DATABASE"),
        "USER": env("SQL_USER"),
        "PASSWORD": env("SQL_PASSWORD"),
        "HOST": env("SQL_HOST"),
        "PORT": env("SQL_PORT"),
    }
}
