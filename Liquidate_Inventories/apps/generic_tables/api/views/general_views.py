from rest_framework import viewsets
from apps.generic_tables.api.serializers.general_serializer import *

class MeasureUnitsViewSet(viewsets.ModelViewSet):
    serializer_class = MeasureUnitsSerializer
    
    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk,state = True).first()
        

class ParameterViewSet(viewsets.ModelViewSet):
    serializer_class = parameterSerializer
    
    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk,state = True).first()
        

class AttributesViewSet(viewsets.ModelViewSet):
    serializer_class = AttributesSerializer
    
    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk,state = True).first()
        
      