from rest_framework.routers import  DefaultRouter
from apps.generic_tables.api.views.options_viewset import OptionViewSet


router = DefaultRouter()
router.register('options', OptionViewSet, basename='Opciones')
urlpatterns =  router.urls