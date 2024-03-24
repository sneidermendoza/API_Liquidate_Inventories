from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/',include('apps.users.api.urls')),
    path('role/',include('apps.users.api.urls')),
    path('generic/',include('apps.generic_tables.api.urls')),
    path('product/',include('apps.products.api.routers')),
]
