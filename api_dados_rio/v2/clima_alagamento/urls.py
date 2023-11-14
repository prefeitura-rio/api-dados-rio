# -*- coding: utf-8 -*-
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"alagamento_15min",
    views.Last15MinFloodView,
    basename="alagamento_15min",
)
router.register(
    r"ultima_atualizacao_alagamento_15min",
    views.LastUpdate15MinFloodView,
    basename="ultima_atualizacao_alagamento_15min",
)
router.register(
    r"alagamento_120min",
    views.Last120MinFloodView,
    basename="alagamento_120min",
)
router.register(
    r"ultima_atualizacao_alagamento_120min",
    views.LastUpdate120MinFloodView,
    basename="ultima_atualizacao_alagamento_120min",
)
router.register(
    r"alagamento_detectado_ia",
    views.AIFloodingDetectionView,
    basename="alagamento_detectado_ia",
)
router.register(
    r"ultima_atualizacao_alagamento_detectado_ia",
    views.LastUpdateAIFloodingDetectionView,
    basename="ultima_atualizacao_alagamento_detectado_ia",
)
