# -*- coding: utf-8 -*-
from .base import *

# Cache
# https://docs.djangoproject.com/en/4.1/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",  # Local Link provided by the redis-server command
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
