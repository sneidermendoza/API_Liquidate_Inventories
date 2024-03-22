from django.urls import path
from apps.users.api.api import custom_user_api_view,role_api_view,custom_user_detail_api_view,role_detail_api_view
urlpatterns = [
    path('usuario/', custom_user_api_view, name= 'usuario_api'),
    path('usuario/<int:pk>/', custom_user_detail_api_view, name= 'detalle_usuario'),
    path('role/', role_api_view, name= 'rol_api'),
    path('role/<int:pk>/', role_detail_api_view, name= 'detalle_rol'),
]
