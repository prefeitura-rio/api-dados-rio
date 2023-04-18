# -*- coding: utf-8 -*-
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"precipitacao_15min",
    views.Last15MinRainView,
    basename="precipitacao_15min",
)
router.register(
    r"ultima_atualizacao_precipitacao_15min",
    views.LastUpdateRainView,
    basename="ultima_atualizacao_precipitacao_15min",
)
