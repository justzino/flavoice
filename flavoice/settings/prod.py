from .base import *  # noqa

DEBUG = env.bool("DEBUG", False)
env.read_env(os.path.join(BASE_DIR, "envs/.env.prod"))

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
THIRD_PARTY_APPS += [
]

# dj-rest-auth 설정: 회원가입 이후 이동할 URL
LOGIN_URL = 'https://flavoice.shop/accounts/login'
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
