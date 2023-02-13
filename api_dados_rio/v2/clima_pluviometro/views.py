# -*- coding: utf-8 -*-
from os import getenv

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from redis_pal import RedisPal
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

CACHE_TTL_SHORT = getattr(settings, "CACHE_TTL_SHORT", DEFAULT_TIMEOUT)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna a quantidade de chuva precipitada em cada hexágono (H3)",
        operation_description="""
        **Resultado**: Retorna uma lista contendo todos os hexágonos (H3) com a quantidade de chuva
        precipitada para os últimos 15 minutos, em milímetros (mm):

        ```json
        [
            {
                "id_h3": "88a8a03989fffff",
                "bairro": "Guaratiba",
                "chuva_15min": 0.0,
                "estacoes": null,
                "status": "sem chuva",
                "color": "#ffffff"
            },
            ...
        ]
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
    ),
)
class Last15MinRainView(LoggingMixin, ViewSet):
    def list(self, request):
        cache_key = "cache_last_15min_rain"
        data_key = "data_last_15min_rain"
        if cache_key in cache:
            data = cache.get(cache_key)
            return Response(data)
        try:
            redis_url = getenv("REDIS_URL")
            assert redis_url is not None
            redis = RedisPal.from_url(redis_url)
            data = redis.get(data_key)
            assert data is not None
            assert isinstance(data, list)
            assert len(data) > 0
            cache.set(cache_key, data, timeout=CACHE_TTL_SHORT)
            return Response(data)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna o horário de atualização dos dados de chuva",
        operation_description="""
        **Resultado**: Retorna um texto contendo o horário de atualização dos dados de chuva:

        ```
        ""
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
    ),
)
class LastUpdateRainView(LoggingMixin, ViewSet):
    def list(self, request):
        rain_cache_key = "cache_last_15min_rain"
        cache_key = "cache_last_15min_rain_update"
        data_key = "data_last_15min_rain_update"
        if rain_cache_key in cache:
            data = cache.get(cache_key)
            return Response(data)
        try:
            redis_url = getenv("REDIS_URL")
            assert redis_url is not None
            redis = RedisPal.from_url(redis_url)
            data = redis.get(data_key)
            assert data is not None
            assert isinstance(data, list)
            assert len(data) > 0
            result = data[0]
            assert "last_update" in result
            last_update = result["last_update"]
            last_update_str = last_update.strftime("%d/%m/%Y %H:%M:%S")
            cache.set(cache_key, last_update_str, timeout=CACHE_TTL_SHORT)
            return Response(last_update_str)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )
