from rest_framework.routers import DefaultRouter
from apps.inventories.api.views.inventory_viewset import *


router = DefaultRouter()


router.register('inventory', InventoriesViewSet, basename= 'inventory' )

urlpatterns = router.urls