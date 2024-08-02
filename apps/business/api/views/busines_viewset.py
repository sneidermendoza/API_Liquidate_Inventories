from django.shortcuts import get_object_or_404
from apps.business.models import Business
from apps.business.api.serializers.business_serializer import *
from rest_framework import viewsets
from rest_framework import status
from apps.helper.api_response_generic import api_response
from django.db.models import Q
from unidecode import unidecode
class  BusinessViewSet(viewsets.GenericViewSet):
    Business = Business
    serializer_class = BusinessSerializer
    queryset = None
    
    def get_object(self,pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
         return self.get_serializer().Meta.model.objects.filter(state = True)
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('-created_date'))
        search = self.request.query_params.get('search')
        if search:
            search_normalized = unidecode(search).lower()
            queryset = queryset.filter(
                Q(name_business__icontains=search_normalized)|
                Q(user__name__icontains=search)
                )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': serializer.data
            }
            return api_response(paginated_response, 'Negocios Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            return api_response(serializer.data, 'Negocios Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')

    def create(self, request):
        business_serializer= self.serializer_class(data = request.data)
        if business_serializer.is_valid():
            business_serializer.save()
            return api_response(business_serializer.data,'Negocio Creado Exitosamente!', status.HTTP_201_CREATED ,None)
        return api_response([],None, status.HTTP_400_BAD_REQUEST,business_serializer.errors )
    
    def retrieve(self, request, pk=None):
        business = self.get_object(pk)
        business_serializer = self.serializer_class(business)
        return api_response(business_serializer.data,'Negocio Obtenido Exitosamente!',status.HTTP_200_OK,None)
    
    def update(self,request, pk=None):
        business = self.get_object(pk)
        business_serializer = UpdateBusinessSerializer(business, data=request.data)
        if business_serializer.is_valid():
            business_serializer.save()
            return api_response(business_serializer.data,"Negocio Actualizado Correctamente",status.HTTP_200_OK,None)           
        return api_response([],None,status.HTTP_200_OK,business_serializer.errors)           
    
    def destroy(self, request, pk=None):
        business_destroy = self.Business.objects.filter(id = pk).update(state= False)
        if business_destroy == 1:
            return api_response([], 'Usuario Eliminado Correctamente',status.HTTP_200_OK,None)
        return api_response([], None,status.HTTP_404_NOT_FOUND,'El Usuario Que Desea Eliminar No Fue Encontrado')
    