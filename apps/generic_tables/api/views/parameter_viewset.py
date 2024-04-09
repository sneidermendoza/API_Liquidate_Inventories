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
        parameter_serializer = self.get_serializer(queryset, many=True)
        
        if queryset.exists():
            return api_response(parameter_serializer.data,'parametros Obtenidos Exitosamente!',status.HTTP_200_OK)
        return api_response([],'No se encontraron registros',status.HTTP_404_NOT_FOUND)
        
    
    def create(self, request):
        parameter_serializer= self.serializer_class(data = request.data)
        if parameter_serializer.is_valid():
            parameter_serializer.save()
            return api_response(parameter_serializer.data,'Parametro Creado Exitosamente!', status.HTTP_201_CREATED )
        return api_response([],parameter_serializer.errors, status.HTTP_400_BAD_REQUEST )
    
    def retrieve(self, request, pk=None):
        parameter = self.get_object(pk)
        parameter_serializer = self.serializer_class(parameter)
        return api_response(parameter_serializer.data,'Parametro Obtenido Exitosamente!',status.HTTP_200_OK)
    
    def update(self,request, pk=None):
        parameter = self.get_object(pk)
        parameter_serializer = self.serializer_class(parameter, data=request.data)
        if parameter_serializer.is_valid():
            parameter_serializer.save()
            return api_response(parameter_serializer.data,"Parametro Actualizado Correctamente",status.HTTP_200_OK)           
        return api_response([],parameter_serializer.errors,status.HTTP_200_OK)           


    def destroy(self, request, pk=None):
        parameter = self.Menu.objects.filter(id = pk).update(state= False)
        if parameter == 1:
            return api_response([], 'Parametro Eliminado Correctamente',status.HTTP_200_OK)
        return api_response([], 'El Parametro Que Desea Eliminar No Fue Encontrado',status.HTTP_404_NOT_FOUND)
    