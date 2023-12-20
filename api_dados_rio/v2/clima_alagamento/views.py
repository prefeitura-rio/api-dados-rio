# -*- coding: utf-8 -*-
from os import getenv

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from redis_pal import RedisPal
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from api_dados_rio.v2.clima_alagamento.utils import get_skupper_redis_client


# Views for last 15 min
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna a quantidade de alagamento em cada hexágono (H3) nos últimos 15 minutos",
        operation_description="""
        **Resultado**: Retorna uma lista contendo todos os hexágonos (H3) e sua respectiva
         quantidade de alagamento para os últimos 15 minutos:

        ```json
        [
            {
                "id_h3": "88a8a03989fffff",
                "bairro": "Guaratiba",
                "qnt_alagamentos": 0.0,
                "estacoes": null,
                "status": "sem alagamento",
                "color": "#ffffff"
            },
            ...
        ]
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
    ),
)
class Last15MinFloodView(LoggingMixin, ViewSet):
    def list(self, request):
        data_key = "data_alagamento_recente_comando"
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
        operation_summary="Retorna o horário de atualização dos dados de alagamento de 15 minutos",
        operation_description="""
        **Resultado**: Retorna um texto contendo o horário de atualização dos dados de alagamento de 15 minutos:

        ```
        ""
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
    ),
)
class LastUpdate15MinFloodView(LoggingMixin, ViewSet):
    def list(self, request):
        last_update_key = "data_update_alagamento_recente_comando"
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
        operation_summary="Retorna a quantidade de alagamento em cada hexágono (H3) nos últimos 120 minutos",
        operation_description="""
        **Resultado**: Retorna uma lista contendo todos os hexágonos (H3) e sua respectiva
         quantidade de alagamento para os últimos 120 minutos:

        ```json
        [
            {
                "id_h3": "88a8a03989fffff",
                "bairro": "Guaratiba",
                "qnt_alagamentos": 0.0,
                "estacoes": null,
                "status": "sem alagamento",
                "color": "#ffffff"
            },
            ...
        ]
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
    ),
)
class Last120MinFloodView(LoggingMixin, ViewSet):
    def list(self, request):
        data_key = "data_alagamento_passado_comando"
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
        operation_summary="Retorna o horário de atualização dos dados de alagamento de 120 minutos",
        operation_description="""
        **Resultado**: Retorna um texto contendo o horário de atualização dos dados de alagamento de 120 minutos:

        ```
        ""
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
    ),
)
class LastUpdate120MinFloodView(LoggingMixin, ViewSet):
    def list(self, request):
        last_update_key = "data_update_alagamento_passado_comando"
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


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna as informações identificadas nas câmeras por IA.",
        operation_description="""
        **Resultado**: Retorna uma lista contendo todas as informações detectados por IA pelas
        câmeras da cidade no seguinte formato:

        ```json
        [
            {
                "datetime": "",
                "id_camera": "",
                "url_camera": "",
                "latitude": 0.0,
                "longitude": 0.0,
                "image_base64": "",
                "ai_classification": [
                    {
                        "object": "alagamento",
                        "label": false,
                        "confidence": "",
                    },
                    ...
                ],
            },
            ...
        ]
        ```
        """,
    ),
)
class AIFloodingDetectionView(LoggingMixin, ViewSet):
    def list(self, request):
        data_key = "flooding_detection_data"
        try:
            redis = get_skupper_redis_client()
            # Get data and set cache
            data = redis.get(data_key)
            assert data is not None
            assert isinstance(data, list)
            return Response(data)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Retorna o horário de atualização dos pontos detectados por IA.",
        operation_description="""
        **Resultado**: Retorna um texto contendo o horário de atualização dos pontos detectados por IA.
        """,
    ),
)
class LastUpdateAIFloodingDetectionView(LoggingMixin, ViewSet):
    def list(self, request):
        last_update_key = "flooding_detection_last_update"
        try:
            redis = get_skupper_redis_client()
            data = redis.get(last_update_key)
            assert data is not None
            return Response(data)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )
