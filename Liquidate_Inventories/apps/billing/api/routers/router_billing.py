from rest_framework.routers import  DefaultRouter
from apps.billing.api.views.billing_viewset import BillingViewSet


router = DefaultRouter()
router.register('', BillingViewSet, basename='Facturacion')
urlpatterns =  router.urls