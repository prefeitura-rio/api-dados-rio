# -*- coding: utf-8 -*-
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"atividades_evento", views.AtividadesEventoView, basename="atividades_evento"
)
router.register(r"atividades_pop", views.AtividadesPopView, basename="atividades_pop")
router.register(r"eventos", views.EventosView, basename="eventos")
router.register(
    r"eventos_abertos", views.EventosAbertosView, basename="eventos_abertos"
)
router.register(r"pops", views.PopsView, basename="pops")
