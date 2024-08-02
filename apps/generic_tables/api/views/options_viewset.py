from rest_framework import viewsets
from apps.generic_tables.api.serializers.options_serializer import OptionSerializer
from django.shortcuts import get_object_or_404
from apps.generic_tables.api.serializers.menus_serializer import MenuSerializer
from apps.generic_tables.models import Options
from apps.helper.api_response_generic import api_response
from rest_framework import status
from unidecode import unidecode
from django.db.models import Q

class OptionViewSet(viewsets.GenericViewSet):
    serializer_class = OptionSerializer
    Opcion = Options
    queryset = None
    
    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
                            
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('-created_date'))
        page = self.paginate_queryset(queryset)
        search = self.request.query_params.get('search')
        if search:
            search_normalized = unidecode(search).lower()
            queryset = queryset.filter(
                Q(name__icontains=search_normalized)
                )
        if page is not None:
            option_serializer = self.get_serializer(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': option_serializer.data
            }
            return api_response(paginated_response, 'Opcion Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        option_serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            return api_response(option_serializer.data, 'Opcion Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')
    
    
    def create(self, request):
        option_serializer= self.serializer_class(data = request.data)
        if option_serializer.is_valid():
            option_serializer.save()
            return api_response(option_serializer.data,'Opcion Creada Exitosamente!', status.HTTP_201_CREATED,None )
        return api_response([],None, status.HTTP_400_BAD_REQUEST,option_serializer.errors )
    
    def retrieve(self, request, pk=None):
        option = self.get_object(pk)
        option_serializer = self.serializer_class(option)
        return api_response(option_serializer.data,'Opcion Obtenida Exitosamente!',status.HTTP_200_OK,None)
    
    def update(self,request, pk=None):
        option = self.get_object(pk)
        option_serializer = self.serializer_class(option, data=request.data)
        if option_serializer.is_valid():
            option_serializer.save()
            return api_response(option_serializer.data,"Opcion Actualizado Correctamente",status.HTTP_200_OK,None)           
        return api_response([],None,status.HTTP_200_OK,option_serializer.errors)           


    def destroy(self, request, pk=None):
        option_destroy = self.Opcion.objects.filter(id = pk).update(state= False)
        if option_destroy == 1:
            return api_response([], 'Opcion Eliminada Correctamente',status.HTTP_200_OK,None)
        return api_response([], None,status.HTTP_404_NOT_FOUND,'El Opcion Que Desea Eliminar No Fue Encontrada')
    