# -*- coding: utf-8 -*-
# reverting
from rest_framework import routers

from api_dados_rio.v2.clima_pluviometro import views

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
# router.register(
#     r"precipitacao_30min",
#     views.Last30MinRainView,
#     basename="precipitacao_30min",
# )
# router.register(
#     r"ultima_atualizacao_precipitacao_30min",
#     views.LastUpdate30MinRainView,
#     basename="ultima_atualizacao_precipitacao_30min",
# )
# router.register(
#     r"precipitacao_60min",
#     views.Last60MinRainView,
#     basename="precipitacao_60min",
# )
# router.register(
#     r"ultima_atualizacao_precipitacao_60min",
#     views.LastUpdate60MinRainView,
#     basename="ultima_atualizacao_precipitacao_60min",
# )
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
# router.register(
#     r"precipitacao_3h",
#     views.Last3HRainView,
#     basename="precipitacao_3h",
# )
# router.register(
#     r"ultima_atualizacao_precipitacao_3h",
#     views.LastUpdate3HRainView,
#     basename="ultima_atualizacao_precipitacao_3h",
# )
# router.register(
#     r"precipitacao_6h",
#     views.Last6HRainView,
#     basename="precipitacao_6h",
# )
# router.register(
#     r"ultima_atualizacao_precipitacao_6h",
#     views.LastUpdate6HRainView,
#     basename="ultima_atualizacao_precipitacao_6h",
# )
# router.register(
#     r"precipitacao_12h",
#     views.Last12HRainView,
#     basename="precipitacao_12h",
# )
# router.register(
#     r"ultima_atualizacao_precipitacao_12h",
#     views.LastUpdate12HRainView,
#     basename="ultima_atualizacao_precipitacao_12h",
# )
# router.register(
#     r"precipitacao_24h",
#     views.Last24HRainView,
#     basename="precipitacao_24h",
# )
# router.register(
#     r"ultima_atualizacao_precipitacao_24h",
#     views.LastUpdate24HRainView,
#     basename="ultima_atualizacao_precipitacao_24h",
# )
# router.register(
#     r"precipitacao_96h",
#     views.Last96HRainView,
#     basename="precipitacao_96h",
# )
# router.register(
#     r"ultima_atualizacao_precipitacao_96h",
#     views.LastUpdate96HRainView,
#     basename="ultima_atualizacao_precipitacao_96h",
# )
