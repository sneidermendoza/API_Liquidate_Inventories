from rest_framework import viewsets
from apps.generic_tables.api.serializers.measure_units_serializer import MeasureUnitsSerializer
from django.shortcuts import get_object_or_404
from apps.generic_tables.api.serializers.menus_serializer import MenuSerializer
from apps.generic_tables.models import MeasureUnits
from apps.helper.api_response_generic import api_response
from rest_framework import status

class MeasureUnitsViewSet(viewsets.GenericViewSet):
    serializer_class = MeasureUnitsSerializer
    Measure_units = MeasureUnits
    queryset = None
    
    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
                            
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        measure_units_serializer = self.get_serializer(queryset, many=True)
        
        if queryset.exists():
            return api_response(measure_units_serializer.data,'Unidades de medidas Obtenidas Exitosamente!',status.HTTP_200_OK,None)
        return api_response([],None,status.HTTP_404_NOT_FOUND,'No se encontraron registros')
        
    
    def create(self, request):
        measure_units_serializer= self.serializer_class(data = request.data)
        if measure_units_serializer.is_valid():
            measure_units_serializer.save()
            return api_response(measure_units_serializer.data,'Unidad de Medida Creada Exitosamente!', status.HTTP_201_CREATED,None )
        return api_response([],None, status.HTTP_400_BAD_REQUEST,measure_units_serializer.errors )
    
    def retrieve(self, request, pk=None):
        measure_units = self.get_object(pk)
        measure_units_serializer = self.serializer_class(measure_units)
        return api_response(measure_units_serializer.data,'Unidad de Medida Obtenida Exitosamente!',status.HTTP_200_OK,None)
    
    def update(self,request, pk=None):
        measure_units = self.get_object(pk)
        measure_units_serializer = self.serializer_class(measure_units, data=request.data)
        if measure_units_serializer.is_valid():
            measure_units_serializer.save()
            return api_response(measure_units_serializer.data,"Unidad de Medida Actualizada Correctamente",status.HTTP_200_OK,None)           
        return api_response([],None,status.HTTP_200_OK,measure_units_serializer.errors)           


    def destroy(self, request, pk=None):
        measure_units_destroy = self.Measure_units.objects.filter(id = pk).update(state= False)
        if measure_units_destroy == 1:
            return api_response([], 'Unidad de Medida Eliminada Correctamente',status.HTTP_200_OK,None)
        return api_response([], None,status.HTTP_404_NOT_FOUND,'La Unidad de Medida Que Desea Eliminar No Fue Encontrado')
    