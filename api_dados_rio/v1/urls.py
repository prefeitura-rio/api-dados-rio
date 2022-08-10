# -*- coding: utf-8 -*-
from functools import partial

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import include, path

from .comando.urls import router as comando_router

SUBROUTERS = {
    "comando/": comando_router,
}
DOCS_LINKS = [
    ("Docs (Swagger)", "/swagger/"),
    ("Docs (redoc)", "/redoc/"),
]


def home(request):
    return render(
        request,
        "index.html",
        {
            "subrouters": list(SUBROUTERS.keys()),
            "version": "(v1)",
            "docs_links": DOCS_LINKS,
        },
    )


def redirect(request, path):
    return HttpResponseRedirect(path)


def generate_urlpatterns():
    urlpatterns = [
        path("", home),
    ]
    for router_path, router in SUBROUTERS.items():
        urlpatterns.append(path(router_path, include(router.urls)))
    return urlpatterns


urlpatterns = generate_urlpatterns()
