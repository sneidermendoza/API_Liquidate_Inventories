from rest_framework import viewsets
from apps.generic_tables.api.serializers.parameter_serializer import ParameterSerializer
from django.shortcuts import get_object_or_404
from apps.generic_tables.api.serializers.menus_serializer import MenuSerializer
from apps.generic_tables.models import Parameter
from apps.helper.api_response_generic import api_response
from rest_framework import status

class ParameterViewSet(viewsets.GenericViewSet):
    serializer_class = ParameterSerializer
    Parameter = Parameter
    queryset = None
    
    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
                            
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            parameter_serializer = self.get_serializer(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': parameter_serializer.data
            }
            return api_response(paginated_response, 'parametros Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        parameter_serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            return api_response(parameter_serializer.data, 'parametros Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')

    
    def create(self, request):
        parameter_serializer= self.serializer_class(data = request.data)
        if parameter_serializer.is_valid():
            parameter_serializer.save()
            return api_response(parameter_serializer.data,'Parametro Creado Exitosamente!', status.HTTP_201_CREATED ,None)
        return api_response([],None, status.HTTP_400_BAD_REQUEST,parameter_serializer.errors )
    
    def retrieve(self, request, pk=None):
        parameter = self.get_object(pk)
        parameter_serializer = self.serializer_class(parameter)
        return api_response(parameter_serializer.data,'Parametro Obtenido Exitosamente!',status.HTTP_200_OK,None)
    
    def update(self,request, pk=None):
        parameter = self.get_object(pk)
        parameter_serializer = self.serializer_class(parameter, data=request.data)
        if parameter_serializer.is_valid():
            parameter_serializer.save()
            return api_response(parameter_serializer.data,"Parametro Actualizado Correctamente",status.HTTP_200_OK,None)           
        return api_response([],None,status.HTTP_200_OK,parameter_serializer.errors)           


    def destroy(self, request, pk=None):
        parameter = self.Parameter.objects.filter(id = pk).update(state= False)
        if parameter == 1:
            return api_response([], 'Parametro Eliminado Correctamente',status.HTTP_200_OK,None)
        return api_response([], None,status.HTTP_404_NOT_FOUND,'El Parametro Que Desea Eliminar No Fue Encontrado')
    