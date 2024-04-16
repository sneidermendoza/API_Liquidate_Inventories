from rest_framework.routers import DefaultRouter
from apps.users.api.views.users_viewset import *

router = DefaultRouter()


router.register('users', CustomUserViewSet, basename= 'users' )

urlpatterns = router.urls