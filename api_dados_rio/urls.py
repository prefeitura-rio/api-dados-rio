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
from django.http import HttpResponseRedirect
from django.urls import include, path
from api_dados_rio.v1.urls import urlpatterns as v1_urlpatterns


def home_view(request):
    return HttpResponseRedirect("/v1/")


urlpatterns = [
    path("", home_view),
    path("v1/", include(v1_urlpatterns)),
]
