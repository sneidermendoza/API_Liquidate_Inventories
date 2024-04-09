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
        roles = self.get_queryset()
        role_serializer = self.list_serializer_class(roles, many =True)
        return api_response(role_serializer.data,'Roles Obtenidos Exitosamente!', status.HTTP_200_OK )
    
    def create(self, request):
        rol_serializer= self.serializer_class(data = request.data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return api_response(rol_serializer.data,'Rol Creado Exitosamente!', status.HTTP_201_CREATED )
        return api_response([],rol_serializer.errors, status.HTTP_400_BAD_REQUEST )
    
    def retrieve(self, request, pk=None):
        role = self.get_object(pk)
        role_serializer = self.serializer_class(role)
        return api_response(role_serializer.data,'Rol Obtenido Exitosamente!',status.HTTP_200_OK)
    
    def update(self,request, pk=None):
        role = self.get_object(pk)
        role_serializer = UpdateRoleSerializer(role, data=request.data)
        if role_serializer.is_valid():
            role_serializer.save()
            return api_response(role_serializer.data,"Rol Actualizado Correctamente!",status.HTTP_200_OK)           
        return api_response([],role_serializer.errors,status.HTTP_200_OK)           

    def destroy(self, request, pk=None):
        role_destroy = self.Role.objects.filter(id = pk).update(status= False)
        if role_destroy == 1:
            return api_response([], 'Rol Eliminado Correctamente',status.HTTP_200_OK)
        return api_response([], 'El Rol Que Desea Eliminar No Fue Encontrado',status.HTTP_404_NOT_FOUND)
    
    