# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from os import getenv
from typing import Any, Dict, List

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from redis_pal import RedisPal
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin


def get_next_update_datetime(base_datetime: datetime = None):
    """
    Updates are done in the following minutes: 8, 18, 28, 38, 48, 58
    We need to calculate the next update time based on the base datetime.
    """
    base_datetime = base_datetime or datetime.now()
    next_update = base_datetime.replace(minute=8, second=0, microsecond=0)
    while next_update <= base_datetime:
        next_update += timedelta(minutes=10)
    return next_update


def get_cache_ttl_seconds(base_datetime: datetime = None):
    """
    Cache TTL is the difference between the next update time and the base datetime.
    """
    base_datetime = base_datetime or datetime.now()
    next_update = get_next_update_datetime(base_datetime)
    return (next_update - base_datetime).total_seconds()


def get_data_from_cache(
    return_data: str,
    data_key: str = "data_last_15min_rain",
    data_cache_key: str = "cache_last_15min_rain",
    last_update_key: str = "data_last_15min_rain_update",
    last_update_cache_key: str = "cache_last_15min_rain_update",
) -> List[Dict[str, Any]]:
    if return_data not in ["data", "last_update"]:
        raise ValueError("return_data must be 'data' or 'last_update'")
    if data_cache_key in cache and last_update_cache_key in cache:
        if return_data == "data":
            data = cache.get(data_cache_key)
            return data
        elif return_data == "last_update":
            last_update = cache.get(last_update_cache_key)
            return last_update
    try:
        cache_ttl = get_cache_ttl_seconds()
        redis_url = getenv("REDIS_URL")
        assert redis_url is not None
        redis = RedisPal.from_url(redis_url)
        # Get data and set cache
        data = redis.get(data_key)
        assert data is not None
        assert isinstance(data, list)
        assert len(data) > 0
        cache.set(data_cache_key, data, timeout=cache_ttl)
        # Get last update and set cache
        data = redis.get(last_update_key)
        assert data is not None
        assert isinstance(data, list)
        assert len(data) > 0
        result = data[0]
        assert "last_update" in result
        last_update = result["last_update"]
        last_update_str = last_update.strftime("%d/%m/%Y %H:%M:%S")
        cache.set(last_update_cache_key, last_update_str, timeout=cache_ttl)
        if return_data == "data":
            return data
        elif return_data == "last_update":
            return last_update_str
    except Exception:
        return []


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
        data = get_data_from_cache("data")
        if data != []:
            return Response(data)
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
        last_update = get_data_from_cache("last_update")
        if last_update != []:
            return Response(last_update)
        return Response(
            {"error": "Something went wrong. Try again later."},
            status=500,
        )
