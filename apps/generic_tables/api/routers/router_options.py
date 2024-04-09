from rest_framework.routers import  DefaultRouter
from apps.generic_tables.api.views.options_viewset import OptionViewSet


router = DefaultRouter()
router.register('', OptionViewSet, basename='Opciones')
urlpatterns =  router.urls