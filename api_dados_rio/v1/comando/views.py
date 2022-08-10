# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Dict, List

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import requests
from requests.adapters import HTTPAdapter, Retry
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

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


class PopsView(ViewSet):
    def list(self, request):
        key = "pops"
        url = getattr(settings, "API_URL_LIST_POPS")
        # Hit cache
        if key in cache:
            pops = cache.get(key)
            return Response(pops)
        result = get_url(url)
        if "error" in result and result["error"]:
            return Response(
                {"error": "Something went wrong. Try again later."}, status=500
            )
        cache.set(key, result, timeout=CACHE_TTL_LONG)
        return Response(result)


class EventosAbertosView(ViewSet):
    def list(self, request):
        key = "eventos_abertos"
        url = getattr(settings, "API_URL_LIST_EVENTOS_ABERTOS")
        # Hit cache
        if key in cache:
            pops = cache.get(key)
            return Response(pops)
        result = get_url(url)
        if "error" in result and result["error"]:
            return Response(
                {"error": "Something went wrong. Try again later."}, status=500
            )
        cache.set(key, result, timeout=CACHE_TTL_SHORT)
        return Response(result)


class EventosView(ViewSet):
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
            return Response({"error": 'Parameter "inicio" is required.'}, status=400)
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
        result = get_url(url, parameters=date_range)
        # If something happened, just return a 500
        if "error" in result and result["error"]:
            return Response(
                {"error": "Something went wrong. Try again later."}, status=500
            )
        # Now we need to check for overlaps in data (and also cache it)
        cache_dates: Dict[str, List] = {}
        for evento in result["eventos"]:
            # Parse the date
            evento_date = datetime.strptime(evento["inicio"], date_format)
            # Reset to midnight
            evento_date = evento_date.replace(hour=0, minute=0, second=0, microsecond=0)
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


class AtividadesEventoView(ViewSet):
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
        result = get_url(url)
        if "error" in result and result["error"]:
            return Response({"error": "Something went wrong. Try again later."})
        cache.set(key, result, timeout=CACHE_TTL_SHORT)
        return Response(result)


class AtividadesPopView(ViewSet):
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
        result = get_url(url)
        if "error" in result and result["error"]:
            return Response({"error": "Something went wrong. Try again later."})
        cache.set(key, result, timeout=CACHE_TTL_LONG)
        return Response(result)
