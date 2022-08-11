# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.urls import include, path

from .cor.urls import urlpatterns as cor_urlpatterns

SUBROUTERS = {}
SUBURLPATTERNS = {"cor/": cor_urlpatterns}
DOCS_LINKS = [
    ("Docs (Swagger)", "/swagger/"),
    ("Docs (redoc)", "/redoc/"),
]


def home(request):
    return render(
        request,
        "index.html",
        {
            "subrouters": list(SUBROUTERS.keys()) + list(SUBURLPATTERNS.keys()),
            "version": "(v1)",
            "docs_links": DOCS_LINKS,
        },
    )


def generate_urlpatterns():
    urlpatterns = [
        path("", home),
    ]
    for router_path, router in SUBROUTERS.items():
        urlpatterns.append(path(router_path, include(router.urls)))
    for urlpatterns_path, urlpatterns_urls in SUBURLPATTERNS.items():
        urlpatterns.append(path(urlpatterns_path, include(urlpatterns_urls)))
    return urlpatterns


urlpatterns = generate_urlpatterns()
