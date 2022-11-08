# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework.views import APIView
from rest_framework.response import Response

from api_dados_rio.custom.routers import IndexRouter
from api_dados_rio.v1 import v1_deprecated
from .comando.urls import router as comando_router

router = IndexRouter(
    routers={"comando": comando_router},
    name="COR",
    deprecated_func=v1_deprecated,
    swagger_operation_summary="Acessa APIs de dados relacionados ao COR (Centro de Operações Rio)",
    swagger_operation_description="",
)

urlpatterns = router.to_urlpatterns()
