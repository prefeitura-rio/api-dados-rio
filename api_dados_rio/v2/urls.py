# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework.views import APIView
from rest_framework.response import Response

from api_dados_rio.custom.routers import IndexRouter
from api_dados_rio.v1 import v1_deprecated
from .adm_cor_comando.urls import router as adm_cor_comando_router

router = IndexRouter(
    routers={"adm_cor_comando": adm_cor_comando_router},
    name="adm_cor_comando",
    swagger_operation_summary="Acessa a versão 2 da API de dados do Escritório de Dados Rio",
    swagger_operation_description="",
)

urlpatterns = router.to_urlpatterns()
