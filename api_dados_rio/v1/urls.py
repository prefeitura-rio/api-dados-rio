# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.urls import include, path

from .comando.urls import router as comando_router

SUBROUTERS = {
    "comando/": comando_router,
}


def home(request):
    return render(
        request,
        "index.html",
        {"subrouters": list(SUBROUTERS.keys()), "version": "(v1)"},
    )


def generate_urlpatterns():
    urlpatterns = [
        path("", home),
    ]
    for router_path, router in SUBROUTERS.items():
        urlpatterns.append(path(router_path, include(router.urls)))
    return urlpatterns


urlpatterns = generate_urlpatterns()
