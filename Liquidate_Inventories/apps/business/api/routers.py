from rest_framework.routers import  DefaultRouter
from apps.business.api.views.busines_viewset import  BusinessViewSet

router = DefaultRouter()

router.register('',BusinessViewSet,basename='business')

urlpatterns = router.urls