# -*- coding: utf-8 -*-
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"precipitacao_15min",
    views.Last15MinRainViewRadar,
    basename="precipitacao_15min",
)
router.register(
    r"ultima_atualizacao_precipitacao_15min",
    views.LastUpdateRainViewRadar,
    basename="ultima_atualizacao_precipitacao_15min",
)
router.register(
    r"precipitacao_120min",
    views.Last120MinRainViewRadar,
    basename="precipitacao_120min",
)
router.register(
    r"ultima_atualizacao_precipitacao_120min",
    views.LastUpdate120MinRainViewRadar,
    basename="ultima_atualizacao_precipitacao_120min",
)
