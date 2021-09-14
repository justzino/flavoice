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

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}