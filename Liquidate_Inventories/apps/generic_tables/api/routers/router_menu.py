from rest_framework.routers import  DefaultRouter
from apps.generic_tables.api.views.menus_viewset import MenuViewSet


router = DefaultRouter()
router.register('', MenuViewSet, basename='Menu')
urlpatterns =  router.urls