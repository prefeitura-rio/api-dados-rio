# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import requests
from requests.adapters import HTTPAdapter, Retry
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
            return Response({"error": "Something went wrong. Try again later."})
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
            return Response({"error": "Something went wrong. Try again later."})
        cache.set(key, result, timeout=CACHE_TTL_SHORT)
        return Response(result)


# class Eventos(ViewSet):
