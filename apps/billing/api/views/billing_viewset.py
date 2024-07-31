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
        queryset = self.filter_queryset(self.get_queryset().order_by('-created_date'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            billing_serializer = self.get_serializer(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': billing_serializer.data
            }
            return api_response(paginated_response, 'Facturas Obtenidas Exitosamente!', status.HTTP_200_OK, None)
        billing_serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            return api_response(billing_serializer.data, 'Facturas Obtenidas Exitosamente!', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')

    
    def create(self, request):
        billing_serializer= self.serializer_class(data = request.data)
        if billing_serializer.is_valid():
            billing_serializer.save()
            return api_response(billing_serializer.data,'factura Creada Exitosamente!', status.HTTP_201_CREATED,None )
        return api_response([],None, status.HTTP_400_BAD_REQUEST,billing_serializer.errors )
    
    def retrieve(self, request, pk=None):
        attributes = self.get_object(pk)
        billing_serializer = self.serializer_class(attributes)
        return api_response(billing_serializer.data,'Factura Obtenida Exitosamente!',status.HTTP_200_OK,None)
    
    def update(self,request, pk=None):
        billing = self.get_object(pk)
        billing_serializer = self.serializer_class(billing, data=request.data)
        if billing_serializer.is_valid():
            billing_serializer.save()
            return api_response(billing_serializer.data,"Factura Actualizada Correctamente",status.HTTP_200_OK,None)           
        return api_response([],None,status.HTTP_200_OK,billing_serializer.errors)           


    def destroy(self, request, pk=None):
        billing_destroy = self.Billing.objects.filter(id = pk).update(state= False)
        if billing_destroy == 1:
            return api_response([], 'Factura Eliminada Correctamente',status.HTTP_200_OK,None)
        return api_response([], None,status.HTTP_404_NOT_FOUND,'La Factura Que Desea Eliminar No Fue Encontrado')
    