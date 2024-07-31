from django.shortcuts import get_object_or_404
from apps.users.models import Role
from apps.users.api.serializers.role_serializer import *
from rest_framework import viewsets
from rest_framework import status
from apps.helper.api_response_generic import api_response

class RoleViewSet(viewsets.ModelViewSet):
    Role = Role
    serializer_class = RoleSerializer
    list_serializer_class = RoleListSerializer
    queryset = None
    
    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.serializer_class().Meta.model.objects\
                            .filter(status = True).values('id','name')
            return self.queryset
    
    def list(self, request):
        roles = self.get_queryset().order_by('-created_at')
        page = self.paginate_queryset(roles)
        if page is not None:
            role_serializer = self.list_serializer_class(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': role_serializer.data
            }
            return api_response(paginated_response, 'Roles Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        if roles.exists():
            role_serializer = self.list_serializer_class(roles, many=True)
            return api_response(role_serializer.data, 'Roles Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')

    def create(self, request):
        rol_serializer= self.serializer_class(data = request.data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return api_response(rol_serializer.data,'Rol Creado Exitosamente!', status.HTTP_201_CREATED, None )
        return api_response([],None, status.HTTP_400_BAD_REQUEST,rol_serializer.errors )
    
    def retrieve(self, request, pk=None):
        role = self.get_object(pk)
        role_serializer = self.serializer_class(role)
        return api_response(role_serializer.data,'Rol Obtenido Exitosamente!',status.HTTP_200_OK, None)
    
    def update(self,request, pk=None):
        role = self.get_object(pk)
        role_serializer = UpdateRoleSerializer(role, data=request.data)
        if role_serializer.is_valid():
            role_serializer.save()
            return api_response(role_serializer.data,"Rol Actualizado Correctamente!",status.HTTP_200_OK, None)           
        return api_response([],None,status.HTTP_400_BAD_REQUEST,role_serializer.errors)           

    def destroy(self, request, pk=None):
        role_destroy = self.Role.objects.filter(id = pk).update(status= False)
        if role_destroy == 1:
            return api_response([], 'Rol Eliminado Correctamente',status.HTTP_200_OK, None)
        return api_response([], None,status.HTTP_404_NOT_FOUND,'El Rol Que Desea Eliminar No Fue Encontrado')
    
    