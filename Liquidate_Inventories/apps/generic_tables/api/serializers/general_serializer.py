from rest_framework import serializers

from apps.generic_tables.models import *

class MeasureUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnits
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)
    
    
class parameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)        

class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)

    def to_representation(self, instance):
        return{ 
            'id' : instance.id,
            'name' : instance.name,
            'parameter_id' : instance.id,
            'parameter_name' : instance.parameter.name,
        }