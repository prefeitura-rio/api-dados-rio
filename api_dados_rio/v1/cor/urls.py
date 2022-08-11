# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.urls import include, path

from .comando.urls import router as comando_router

SUBROUTERS = {
    "comando/": comando_router,
}
DOCS_LINKS = []


def home(request):
    return render(
        request,
        "index.html",
        {
            "subrouters": list(SUBROUTERS.keys()),
            "version": "/cor (v1)",
            "docs_links": DOCS_LINKS,
        },
    )


def generate_urlpatterns():
    urlpatterns = [
        path("", home),
    ]
    for router_path, router in SUBROUTERS.items():
        urlpatterns.append(path(router_path, include(router.urls)))
    return urlpatterns


urlpatterns = generate_urlpatterns()
