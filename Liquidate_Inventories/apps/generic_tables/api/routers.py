from rest_framework.routers import  DefaultRouter
from apps.generic_tables.api.views.general_views import *


router = DefaultRouter()

router.register(r'measure-units', MeasureUnitsViewSet, basename='Unidades de medida')
router.register(r'Attributes', AttributesViewSet, basename='atributos')
router.register(r'parameter', ParameterViewSet, basename='Parametros')

urlpatterns =  router.urls
