# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.urls import include, path

from api_dados_rio.v1 import v1_deprecated
from api_dados_rio.custom.routers import IndexRouter
from .cor.urls import urlpatterns as cor_urlpatterns

SUBURLPATTERNS = {"cor/": cor_urlpatterns}
DOCS_LINKS = [
    ("Docs (Swagger)", "/swagger/"),
    ("Docs (redoc)", "/redoc/"),
]


def generate_urlpatterns():
    urlpatterns = []
    for urlpatterns_path, urlpatterns_urls in SUBURLPATTERNS.items():
        urlpatterns.append(path(urlpatterns_path, include(urlpatterns_urls)))
    return urlpatterns


router = IndexRouter(
    urlpatterns=generate_urlpatterns(),
    name="V1",
    deprecated_func=v1_deprecated,
    swagger_operation_summary="Acessa a versão 1 da API de dados do Escritório de Dados Rio",
    swagger_operation_description="""
    **Aviso:** Essa versão da API será descontinuada a partir de 01/01/2023.
    """,
)

urlpatterns = router.to_urlpatterns()
