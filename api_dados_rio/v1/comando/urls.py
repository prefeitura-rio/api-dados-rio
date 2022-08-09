# -*- coding: utf-8 -*-
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"pops", views.PopsView, basename="pops")
router.register(
    r"eventos_abertos", views.EventosAbertosView, basename="eventos_abertos"
)
