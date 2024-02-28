# -*- coding: utf-8 -*-
from os import getenv

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from redis_pal import RedisPal
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin


# Views for last 5 min
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna a quantidade em mm de chuva precipitada em cada hexágono (H3) nos últimos 5 minutos",
        operation_description="""
        **Resultado**: Retorna uma lista contendo todos os hexágonos (H3) com a quantidade de chuva
        precipitada estimada do radar do INEA para os últimos 5 minutos, em milímetros (mm):

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
        data_key = "data_chuva_recente_radar_inea"
        try:
            redis_url = getenv("REDIS_URL")
            assert redis_url is not None
            redis = RedisPal.from_url(redis_url)
            # Get data and set cache
            data = redis.get(data_key)
            assert data is not None
            assert isinstance(data, list)
            assert len(data) > 0
            return Response(data)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna o horário de atualização dos dados de chuva do radar do INEA dos últimos 5 minutos",
        operation_description="""
        **Resultado**: Retorna um texto contendo o horário de atualização dos dados de chuva do radar do INEA:

        ```
        ""
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
    ),
)
class LastUpdateRainView(LoggingMixin, ViewSet):
    def list(self, request):
        last_update_key = "data_update_chuva_recente_radar_inea"
        try:
            redis_url = getenv("REDIS_URL")
            assert redis_url is not None
            redis = RedisPal.from_url(redis_url)
            data = redis.get(last_update_key)
            assert data is not None
            assert isinstance(data, list)
            assert len(data) > 0
            result = data[0]
            assert "last_update" in result
            last_update = result["last_update"]
            last_update_str = last_update.strftime("%d/%m/%Y %H:%M:%S")
            return Response(last_update_str)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )


# Views for last 120 min
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna a quantidade em mm de chuva precipitada em cada hexágono (H3) nos últimos 120 minutos",
        operation_description="""
        **Resultado**: Retorna uma lista contendo todos os hexágonos (H3) com a quantidade de chuva
        precipitada estimada do radar do INEA para os últimos 120 minutos, em milímetros (mm):

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
class Last120MinRainView(LoggingMixin, ViewSet):
    def list(self, request):
        data_key = "data_chuva_passado_radar_inea"
        try:
            redis_url = getenv("REDIS_URL")
            assert redis_url is not None
            redis = RedisPal.from_url(redis_url)
            # Get data and set cache
            data = redis.get(data_key)
            assert data is not None
            assert isinstance(data, list)
            assert len(data) > 0
            return Response(data)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna o horário de atualização dos dados de chuva do radar do INEA dos últimos 120 minutos",
        operation_description="""
        **Resultado**: Retorna um texto contendo o horário de atualização dos dados de chuva do radar do INEA:

        ```
        ""
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
    ),
)
class LastUpdate120MinRainView(LoggingMixin, ViewSet):
    def list(self, request):
        last_update_key = "data_update_chuva_passado_radar_inea"
        try:
            redis_url = getenv("REDIS_URL")
            assert redis_url is not None
            redis = RedisPal.from_url(redis_url)
            data = redis.get(last_update_key)
            assert data is not None
            assert isinstance(data, list)
            assert len(data) > 0
            result = data[0]
            assert "last_update" in result
            last_update = result["last_update"]
            last_update_str = last_update.strftime("%d/%m/%Y %H:%M:%S")
            return Response(last_update_str)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )
