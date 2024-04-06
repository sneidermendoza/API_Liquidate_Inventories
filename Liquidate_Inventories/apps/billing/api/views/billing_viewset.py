from rest_framework import viewsets
from apps.billing.api.serializers.billing_serializer import BillinSerializer
from django.shortcuts import get_object_or_404
from apps.billing.models import Billings
from apps.helper.api_response_generic import api_response
from rest_framework import status


class BillingViewSet(viewsets.GenericViewSet):
    serializer_class = BillinSerializer
    Billing = Billings
    queryset = None
    
    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
                            
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        billing_serializer = self.get_serializer(queryset, many=True)
        
        if queryset.exists():
            return api_response(billing_serializer.data,'Facturas Obtenidas Exitosamente!',status.HTTP_200_OK)
        return api_response([],'No se encontraron registros',status.HTTP_404_NOT_FOUND)
        
    
    def create(self, request):
        billing_serializer= self.serializer_class(data = request.data)
        if billing_serializer.is_valid():
            billing_serializer.save()
            return api_response(billing_serializer.data,'factura Creada Exitosamente!', status.HTTP_201_CREATED )
        return api_response([],billing_serializer.errors, status.HTTP_400_BAD_REQUEST )
    
    def retrieve(self, request, pk=None):
        attributes = self.get_object(pk)
        billing_serializer = self.serializer_class(attributes)
        return api_response(billing_serializer.data,'Factura Obtenida Exitosamente!',status.HTTP_200_OK)
    
    def update(self,request, pk=None):
        billing = self.get_object(pk)
        billing_serializer = self.serializer_class(billing, data=request.data)
        if billing_serializer.is_valid():
            billing_serializer.save()
            return api_response(billing_serializer.data,"Factura Actualizada Correctamente",status.HTTP_200_OK)           
        return api_response([],billing_serializer.errors,status.HTTP_200_OK)           


    def destroy(self, request, pk=None):
        billing_destroy = self.Billing.objects.filter(id = pk).update(state= False)
        if billing_destroy == 1:
            return api_response([], 'Factura Eliminada Correctamente',status.HTTP_200_OK)
        return api_response([], 'La Factura Que Desea Eliminar No Fue Encontrado',status.HTTP_404_NOT_FOUND)
    