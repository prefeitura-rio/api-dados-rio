# -*- coding: utf-8 -*-
"""api_dados_rio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api_dados_rio.custom.routers import IndexRouter
from api_dados_rio.v1.urls import urlpatterns as v1_urlpatterns
from api_dados_rio.v2.urls import urlpatterns as v2_urlpatterns

# flake8: noqa: E501

schema_view = get_schema_view(
    openapi.Info(
        title="API Dados Rio",
        default_version="v2",
        description="""
        API de dados públicos do Escritório de Dados.

        Em caso de dúvidas, sugestões ou reclamações, favor entrar em contato por um de nossos canais oficiais (https://docs.dados.rio/contato/) ou através do formulário em https://share.dados.rio/services-form.
        """,
        terms_of_service="",
        contact=openapi.Contact(email="escritoriodedados@gmail.com"),
        license=openapi.License(name="GPLv3"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

base_urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthcheck/", include("health_check.urls")),
    path("v1/", include(v1_urlpatterns)),
    path("v2/", include(v2_urlpatterns)),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
    ),
    re_path(
        r"^docs(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
]

router = IndexRouter(
    urlpatterns=base_urlpatterns,
)

urlpatterns = router.to_urlpatterns()
