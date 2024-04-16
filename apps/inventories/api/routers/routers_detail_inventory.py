from rest_framework.routers import DefaultRouter
from apps.inventories.api.views.detail_inventory_viewset import InventoryDetailsViewSet


router = DefaultRouter()

router.register('detail_inventory', InventoryDetailsViewSet, basename= 'detail inventory' )

urlpatterns = router.urls