# -*- coding: utf-8 -*-
from rest_framework import routers

from api_dados_rio.v2.clima_alagamento import views

router = routers.DefaultRouter()
router.register(
    r"cameras",
    views.AIFloodingDetectionView,
    basename="cameras",
)
router.register(
    r"ultima_atualizacao_cameras",
    views.LastUpdateAIFloodingDetectionView,
    basename="ultima_atualizacao_cameras",
)
