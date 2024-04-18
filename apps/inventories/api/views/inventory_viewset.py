from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from apps.inventories.api.serializers.inventory_serializer import *
from apps.helper.api_response_generic import api_response
from apps.inventories.models import Inventories,InventoryDetails

class InventoriesViewSet(viewsets.GenericViewSet):
    Inventory = Inventories
    serializer_class = InventorySerializer
    queryset = None
    
    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
                            
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        if queryset.exists():
            return api_response(serializer.data,'Inventarios Obtenidos Exitosamente!',status.HTTP_200_OK,None)
        return api_response([],None,status.HTTP_404_NOT_FOUND,'No se encontraron registros')
        
    
    def create(self, request):
        inventory_serializer= self.serializer_class(data = request.data)
        if inventory_serializer.is_valid():
            inventory_serializer.save()
            return api_response(inventory_serializer.data,'Inventario Creado Exitosamente!', status.HTTP_201_CREATED,None )
        return api_response([],None, status.HTTP_400_BAD_REQUEST,inventory_serializer.errors )
    
    def retrieve(self, request, pk=None):
        inventory = self.get_object(pk)
        inventory_serializer = self.serializer_class(inventory)
        return api_response(inventory_serializer.data,'Inventario Obtenido Exitosamente!',status.HTTP_200_OK,None)
    
    def update(self,request, pk=None):
        inventory = self.get_object(pk)
        inventory_serializer = UpdateInventorySerializer(inventory, data=request.data)
        if inventory_serializer.is_valid():
            inventory_serializer.save()
            return api_response(inventory_serializer.data,"Inventario Actualizado Correctamente",status.HTTP_200_OK,None)           
        return api_response([],None,status.HTTP_200_OK,inventory_serializer.errors)           


    def destroy(self, request, pk=None):
        inventory_destroy = self.Inventory.objects.filter(id = pk).update(state= False)
        if inventory_destroy == 1:
            return api_response([], 'Usuario Eliminado Correctamente',status.HTTP_200_OK,None)
        return api_response([], None,status.HTTP_404_NOT_FOUND,'El Usuario Que Desea Eliminar No Fue Encontrado')
    