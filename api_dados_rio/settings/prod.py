# -*- coding: utf-8 -*-
from os import getenv

from .base import *

DEBUG = False
SECRET_KEY = getenv("DJANGO_SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": getenv("DB_NAME"),
        "USER": getenv("DB_USER"),
        "PASSWORD": getenv("DB_PASSWORD"),
        "HOST": getenv("DB_HOST"),
        "PORT": getenv("DB_PORT"),
    }
}

# Cache
# https://docs.djangoproject.com/en/4.1/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": getenv("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

ADMINS = [("Gabriel Milan", "gabriel.gazola@poli.ufrj.br")]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = getenv("EMAIL_HOST_USER")
SERVER_EMAIL = getenv("EMAIL_HOST_USER")

API_USERNAME = getenv("API_USERNAME")
API_PASSWORD = getenv("API_PASSWORD")
API_URL_LOGIN = getenv("API_URL_LOGIN")
API_URL_LIST_POPS = getenv("API_URL_LIST_POPS")
API_URL_LIST_EVENTOS_ABERTOS = getenv("API_URL_LIST_EVENTOS_ABERTOS")
API_URL_LIST_EVENTOS = getenv("API_URL_LIST_EVENTOS")
API_URL_LIST_ATIVIDADES_EVENTOS = getenv("API_URL_LIST_ATIVIDADES_EVENTOS")
API_URL_LIST_ATIVIDADES_POP = getenv("API_URL_LIST_ATIVIDADES_POP")

REDIS_URL = getenv("REDIS_URL")
