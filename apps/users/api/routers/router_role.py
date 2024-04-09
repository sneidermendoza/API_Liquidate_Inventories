from rest_framework.routers import DefaultRouter
from apps.users.api.views.role_viewset import *

router = DefaultRouter()


router.register('', RoleViewSet, basename= 'roles' )

urlpatterns = router.urls