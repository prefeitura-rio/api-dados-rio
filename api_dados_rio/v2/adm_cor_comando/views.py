# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Dict, List

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import requests
from requests.adapters import HTTPAdapter, Retry
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

# Cache timeout
CACHE_TTL_SHORT = getattr(settings, "CACHE_TTL_SHORT", DEFAULT_TIMEOUT)
CACHE_TTL_LONG = getattr(settings, "CACHE_TTL_LONG", DEFAULT_TIMEOUT)


def get_token():
    """Get token to access comando's API"""
    # Acessar username e password
    host = getattr(settings, "API_URL_LOGIN")
    username = getattr(settings, "API_USERNAME")
    password = getattr(settings, "API_PASSWORD")
    payload = {"username": username, "password": password}
    return requests.post(host, json=payload).text


def get_url(url, parameters: dict = None, token: str = None):  # pylint: disable=W0102
    """Make request to comando's API"""
    if not parameters:
        parameters = {}
    if not token:
        token = get_token()
    sess = requests.Session()
    retries = Retry(total=5, backoff_factor=1.5)
    sess.mount("http://", HTTPAdapter(max_retries=retries))
    headers = {"Authorization": token}

    try:
        response = sess.get(url, json=parameters, headers=headers)
        response = response.json()
    except Exception as exc:
        response = {"error": exc}
    return response


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Lista todos os POPs (Procedimento Operacional Padrão)",
        operation_description="""
        **Resultado**: Retorna uma lista contendo todos os POPs existentes com o seguinte formato:

        ```json
        {
            "retorno": "OK",
            "mensagem": "",
            "objeto": [
                {
                    "titulo": "Abalroamento",
                    "id": 24
                },
                ...
            ]
        }
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 1 dia.
        """,
    ),
)
class PopsView(LoggingMixin, ViewSet):
    def list(self, request):
        key = "pops"
        url = getattr(settings, "API_URL_LIST_POPS")
        # Hit cache
        if key in cache:
            pops = cache.get(key)
            return Response(pops)
        try:
            result = get_url(url)
            if "error" in result and result["error"]:
                return Response(
                    {"error": "Something went wrong. Try again later."},
                    status=500,
                )
            cache.set(key, result, timeout=CACHE_TTL_LONG)
            return Response(result)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Lista todos os eventos abertos no momento",
        operation_description="""
        **Resultado**: Retorna uma lista contendo todos os eventos abertos com o seguinte formato:

        ```json
        {
            "eventos": [
                {
                    "tipo": "SECUNDARIO",
                    "pop_id": 25,
                    "bairro": "Botafogo",
                    "latitude": -22.9513106,
                    "anexos": [],
                    "inicio": "2022-06-09 09:43:26.0",
                    "titulo": "Obra na Via ( Naturgy ) Cam 182",
                    "prazo": "LONGO",
                    "descricao": "R. São Clemente - Alt. n° 355 - Botafogo",
                    "informe_id": 75866,
                    "gravidade": "BAIXO",
                    "id": 75865,
                    "longitude": -43.1942684,
                    "status": "ABERTO",
                },
                ...
            ]
        }
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos. Nesse
        sentido, requisições feitas com intervalo menor que 5 minutos tendem a retornar o mesmo
        resultado. Após 5 minutos, caso não seja possível obter atualizações na origem, essa API
        responderá com o último resultado obtido, inserindo também uma chave `error` no resultado
        dizendo `Failed to fetch new data, using backup cached data.`.
        """,
    ),
)
class EventosAbertosView(LoggingMixin, ViewSet):
    def list(self, request):
        key = "eventos_abertos"
        key_backup = "eventos_abertos_backup"
        url = getattr(settings, "API_URL_LIST_EVENTOS_ABERTOS")
        # Hit cache
        if key in cache:
            pops = cache.get(key)
            return Response(pops)
        try:
            result = get_url(url)
            if "error" in result and result["error"]:
                if key_backup in cache:
                    result = cache.get(key_backup)
                    result[
                        "error"
                    ] = "Failed to fetch new data, using backup cached data."
                    return Response(result)
                return Response(
                    {"error": "Something went wrong. Try again later."},
                    status=500,
                )
            cache.set(key, result, timeout=CACHE_TTL_SHORT)
            cache.set(key_backup, result, timeout=None)
            return Response(result)
        except Exception:
            if key_backup in cache:
                result = cache.get(key_backup)
                result["error"] = "Failed to fetch new data, using backup cached data."
                return Response(result)
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Lista todos os eventos de acordo com os parâmetros informados",
        operation_description="""
        **Resultado**: Retorna uma lista contendo eventos com o seguinte formato:

        ```json
        {
            "eventos": [
                {
                    "tipo": "SECUNDARIO",
                    "pop_id": 25,
                    "bairro": "Botafogo",
                    "latitude": -22.9513106,
                    "anexos": [],
                    "inicio": "2022-06-09 09:43:26.0",
                    "titulo": "Obra na Via ( Naturgy ) Cam 182",
                    "prazo": "LONGO",
                    "descricao": "R. São Clemente - Alt. n° 355 - Botafogo",
                    "informe_id": 75866,
                    "gravidade": "BAIXO",
                    "id": 75865,
                    "longitude": -43.1942684,
                    "status": "ABERTO",
                },
                ...
            ]
        }
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
        manual_parameters=[
            openapi.Parameter(
                "inicio",
                openapi.IN_QUERY,
                description="Data de início da listagem de eventos",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "fim",
                openapi.IN_QUERY,
                description="Data de fim da listagem de eventos (máximo: início + 30 dias)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
    ),
)
class EventosView(LoggingMixin, ViewSet):
    def list(self, request: Request):
        # Set some date formats we're going to use
        date_format = "%Y-%m-%d %H:%M:%S.0"
        redis_date_format = "%Y_%m_%d"
        # These are base stuff we wanna use for fetching data
        base_key = "eventos"
        url = getattr(settings, "API_URL_LIST_EVENTOS")
        # Get parameters from request body
        parameters = request.query_params
        # First parameter is the start date, this is required
        inicio = parameters.get("inicio")
        if not inicio:
            return Response(
                {"error": 'Parameter "inicio" is required.'},
                status=400,
            )
        # Try to parse it from expected date format
        try:
            inicio = datetime.strptime(inicio, date_format)
        except ValueError:
            return Response(
                {"error": f'Parameter "inicio" must be in format {date_format}.'},
                status=400,
            )
        # Reset the date to midnight
        inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        # Second parameter is the end date, this is optional
        fim = parameters.get("fim")
        if fim:
            # Try to parse it from expected date format
            try:
                fim = datetime.strptime(fim, date_format)
            except ValueError:
                return Response(
                    {"error": f'Parameter "fim" must be in format {date_format}.'},
                    status=400,
                )
            fim = fim.replace(hour=0, minute=0, second=0, microsecond=0)
            # Date diff must be less than or equal to 30 days
            if (fim - inicio) > timedelta(days=30):
                return Response(
                    {"error": "(fim - inicio) must be less than or equal to 30 days."},
                    status=400,
                )
        # If end date is not provided, set this to the start date + 30 days
        else:
            fim = inicio + timedelta(days=30)
        # Now we build a list of dates to fetch data for
        dates: List[datetime] = []
        for i in range(int((fim - inicio).days) + 1):
            dates.append(inicio + timedelta(days=i))
        # Keep track of the minimum and maximum dates we're fetching data for
        min_date = None
        max_date = None
        from_cache = []
        results = {"eventos": []}
        # Loop through dates and check if we have data in cache
        for date in dates:
            key = f"{base_key}_{date.strftime(redis_date_format)}"
            # If we find it in cache, add it to the results and continue
            if key in cache:
                result = cache.get(key)
                if result and "eventos" in result:
                    results["eventos"].append(result)
                    from_cache.append(date)
                    continue
            # We're not in cache, save the date to use as a parameter
            if min_date is None or date < min_date:
                min_date = date
            if max_date is None or date > max_date:
                max_date = date
        # If we have everything in cache, return it
        if not min_date and not max_date:
            return Response(results)
        if min_date == max_date:
            max_date += timedelta(days=1)
        # If we don't, fetch data for the date range we're missing
        date_range = {
            "inicio": min_date.strftime(date_format),
            "fim": max_date.strftime(date_format),
        }
        try:
            result = get_url(url, parameters=date_range)
            # If something happened, just return a 500
            if "error" in result and result["error"]:
                return Response(
                    {"error": "Something went wrong. Try again later."},
                    status=500,
                )
            # Now we need to check for overlaps in data (and also cache it)
            cache_dates: Dict[str, List] = {}
            for evento in result["eventos"]:
                # Parse the date
                evento_date = datetime.strptime(evento["inicio"], date_format)
                # Reset to midnight
                evento_date = evento_date.replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                # If this date is not in `from_cache`, add it to the results
                if evento_date not in from_cache:
                    results["eventos"].append(evento)
                # Now we split dates into cache_dates keys and append the evento to the list
                # in the cache_dates key
                if evento_date not in cache_dates:
                    cache_dates[evento_date] = []
                cache_dates[evento_date].append(evento)
            # Finally we loop through cache_dates and cache the data
            for date, eventos in cache_dates.items():
                key = f"{base_key}_{date.strftime(redis_date_format)}"
                cache.set(key, {"eventos": eventos}, timeout=CACHE_TTL_SHORT)
            return Response(results)
        except Exception:
            return Response(
                {"error": "Something went wrong. Try again later."},
                status=500,
            )


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Lista as atividades relacionadas a um evento",
        operation_description="""
        **Resultado**: Retorna uma lista contendo atividades de um evento com o seguinte formato:

        ```json
        {
            "atividades": [
                {
                "orgao": "CET-RIO",
                "chegada": "2022-06-09 09:47:04",
                "inicio": "2022-06-09 09:47:04",
                "nome": "Companhia de Engenharia de Tráfego",
                "descricao": "Monitorar possíveis interdições",
                "status": "PRESENTE"
                },
                ...
            ]
        }
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 5 minutos.
        """,
        manual_parameters=[
            openapi.Parameter(
                "eventoId",
                openapi.IN_QUERY,
                description="ID do evento",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    ),
)
class AtividadesEventoView(LoggingMixin, ViewSet):
    def list(self, request):
        base_key = "atividades_evento"
        base_url = getattr(settings, "API_URL_LIST_ATIVIDADES_EVENTOS")
        evento_id = request.query_params.get("eventoId")
        if not evento_id:
            return Response({"error": "eventoId is required."})
        key = f"{base_key}_{evento_id}"
        url = f"{base_url}?eventoId={evento_id}"
        # Hit cache
        if key in cache:
            atividades = cache.get(key)
            return Response(atividades)
        try:
            result = get_url(url)
            if "error" in result and result["error"]:
                return Response({"error": "Something went wrong. Try again later."})
            cache.set(key, result, timeout=CACHE_TTL_SHORT)
            return Response(result)
        except Exception:
            return Response({"error": "Something went wrong. Try again later."})


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Lista as atividades relacionadas a um POP",
        operation_description="""
        **Resultado**: Retorna uma lista contendo atividades de um POP com o seguinte formato:

        ```json
        {
        "pop": "Bolsão d'água em via",
        "atividades": [
                {
                "sigla": "CET-RIO",
                "orgao": "Companhia de Engenharia de Tráfego",
                "acao": "Desfazer o acidente"
                },
                ...
            ]
        }
        ```

        **Política de cache**: O resultado é armazenado em cache por um período de 1 dia.
        """,
        manual_parameters=[
            openapi.Parameter(
                "popId",
                openapi.IN_QUERY,
                description="ID do POP",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
    ),
)
class AtividadesPopView(LoggingMixin, ViewSet):
    def list(self, request):
        base_key = "atividades_pop"
        base_url = getattr(settings, "API_URL_LIST_ATIVIDADES_POP")
        pop_id = request.query_params.get("popId")
        if not pop_id:
            return Response({"error": "popId is required."})
        key = f"{base_key}_{pop_id}"
        url = f"{base_url}?popId={pop_id}"
        # Hit cache
        if key in cache:
            atividades = cache.get(key)
            return Response(atividades)
        try:
            result = get_url(url)
            if "error" in result and result["error"]:
                return Response({"error": "Something went wrong. Try again later."})
            cache.set(key, result, timeout=CACHE_TTL_LONG)
            return Response(result)
        except Exception:
            return Response({"error": "Something went wrong. Try again later."})
