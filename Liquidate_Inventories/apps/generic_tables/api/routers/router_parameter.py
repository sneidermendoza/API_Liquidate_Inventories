from rest_framework.routers import  DefaultRouter
from apps.generic_tables.api.views.parameter_viewset import ParameterViewSet


router = DefaultRouter()
router.register('', ParameterViewSet, basename='Parametros')
urlpatterns =  router.urls