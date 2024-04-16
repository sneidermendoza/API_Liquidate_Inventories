from rest_framework.routers import  DefaultRouter
from apps.generic_tables.api.views.measure_units_viewset import MeasureUnitsViewSet


router = DefaultRouter()
router.register('measure_units', MeasureUnitsViewSet, basename='Unidades de Medida')
urlpatterns =  router.urls