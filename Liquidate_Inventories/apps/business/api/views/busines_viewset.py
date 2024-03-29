from django.shortcuts import get_object_or_404
from apps.business.models import Business
from apps.business.api.serializers.business_serializer import *
from rest_framework import viewsets
from rest_framework import status
from apps.helper.api_response_generic import api_response

class  BusinessViewSet(viewsets.GenericViewSet):
    Business = Business
    serializer_class = BusinessSerializer
    queryset = None
    
    def get_object(self,pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
         return self.get_serializer().Meta.model.objects.filter(state = True)
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        if queryset.exists():
            return api_response(serializer.data,'Negocios Obtenidos Exitosamente!',status.HTTP_200_OK)
        return api_response([],'No se encontraron registros',status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        business_serializer= self.serializer_class(data = request.data)
        if business_serializer.is_valid():
            business_serializer.save()
            return api_response(business_serializer.data,'Negocio Creado Exitosamente!', status.HTTP_201_CREATED )
        return api_response([],business_serializer.errors, status.HTTP_400_BAD_REQUEST )
    
    def retrieve(self, request, pk=None):
        business = self.get_object(pk)
        business_serializer = self.serializer_class(business)
        return api_response(business_serializer.data,'Negocio Obtenido Exitosamente!',status.HTTP_200_OK)
    
    def update(self,request, pk=None):
        business = self.get_object(pk)
        business_serializer = UpdateBusinessSerializer(business, data=request.data)
        if business_serializer.is_valid():
            business_serializer.save()
            return api_response(business_serializer.data,"Negocio Actualizado Correctamente",status.HTTP_200_OK)           
        return api_response([],business_serializer.errors,status.HTTP_200_OK)           
    
    def destroy(self, request, pk=None):
        business_destroy = self.Business.objects.filter(id = pk).update(state= False)
        if business_destroy == 1:
            return api_response([], 'Usuario Eliminado Correctamente',status.HTTP_200_OK)
        return api_response([], 'El Usuario Que Desea Eliminar No Fue Encontrado',status.HTTP_404_NOT_FOUND)
    