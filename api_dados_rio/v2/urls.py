# -*- coding: utf-8 -*-
from api_dados_rio.custom.routers import IndexRouter
from .adm_cor_comando.urls import router as adm_cor_comando_router
from .clima_alagamento.urls import router as clima_alagamento_router
from .clima_pluviometro.urls import router as clima_pluviometro_router
from .clima_radar.urls import router as clima_radar_router

router = IndexRouter(
    routers={
        "adm_cor_comando": adm_cor_comando_router,
        "clima_alagamento": clima_alagamento_router,
        "clima_pluviometro": clima_pluviometro_router,
        "clima_radar": clima_radar_router,
    },
    name="adm_cor_comando",
    swagger_operation_summary="Acessa a versão 2 da API de dados do Escritório de Dados Rio",
    swagger_operation_description="",
)

urlpatterns = router.to_urlpatterns()
