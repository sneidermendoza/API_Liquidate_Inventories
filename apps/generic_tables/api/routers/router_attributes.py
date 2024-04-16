from rest_framework.routers import  DefaultRouter
from apps.generic_tables.api.views.attributes_viewset import AttributesViewSet


router = DefaultRouter()
router.register('attributes', AttributesViewSet, basename='Atributos')
urlpatterns =  router.urls