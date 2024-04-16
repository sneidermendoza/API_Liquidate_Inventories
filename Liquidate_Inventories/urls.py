from django.contrib import admin
from django.urls import path,include,re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.users.views import Login,Logout


schema_view = get_schema_view(
   openapi.Info(
      title="Inventories API",
      default_version='v1',
      description="Aplicacion para generar inventarios en tiendas",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mariasol0304@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/login/', Login.as_view(),name = 'Login'),
    path('api/logout/', Logout.as_view(),name= 'Logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/',include('apps.users.api.routers.router_user')),
    path('api/',include('apps.users.api.routers.router_role')),
    path('api/',include('apps.generic_tables.api.routers.router_measure_units')),
    path('api/',include('apps.generic_tables.api.routers.router_attributes')),
    path('api/',include('apps.generic_tables.api.routers.router_parameter')),
    path('api/',include('apps.generic_tables.api.routers.router_menu')),
    path('api/',include('apps.generic_tables.api.routers.router_options')),
    path('api/',include('apps.products.api.routers')),
    path('api/',include('apps.business.api.routers')),
    path('api/',include('apps.inventories.api.routers.routers_inventory')),
    path('api/',include('apps.inventories.api.routers.routers_detail_inventory')),
    path('api/',include('apps.billing.api.routers.router_billing')),
]
