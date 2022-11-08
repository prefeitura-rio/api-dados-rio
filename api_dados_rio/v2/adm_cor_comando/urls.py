# -*- coding: utf-8 -*-
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"ocorrencias_orgaos_responsaveis",
    views.AtividadesEventoView,
    basename="ocorrencias_orgaos_responsaveis",
)
router.register(
    r"procedimento_operacional_padrao_orgaos_responsaveis",
    views.AtividadesPopView,
    basename="procedimento_operacional_padrao_orgaos_responsaveis",
)
router.register(r"ocorrencias", views.EventosView, basename="ocorrencias")
router.register(
    r"ocorrencias_abertas", views.EventosAbertosView, basename="ocorrencias_abertas"
)
router.register(r"pops", views.PopsView, basename="procedimento_operacional_padrao")
