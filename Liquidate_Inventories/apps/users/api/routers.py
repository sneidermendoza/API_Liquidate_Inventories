from rest_framework.routers import DefaultRouter
from apps.users.api.views.users_viewset import *
from apps.users.api.views.role_viewset import *

router = DefaultRouter()


router.register('', CustomUserViewSet, basename= 'users' )
router.register('', RoleViewSet, basename= 'roles' )

urlpatterns = router.urls