# -*- coding: utf-8 -*-
from rest_framework import routers

# from api_dados_rio.v2.clima_radar import views
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
router.register(
    r"precipitacao_120min",
    views.Last120MinRainView,
    basename="precipitacao_120min",
)
router.register(
    r"ultima_atualizacao_precipitacao_120min",
    views.LastUpdate120MinRainView,
    basename="ultima_atualizacao_precipitacao_120min",
)
