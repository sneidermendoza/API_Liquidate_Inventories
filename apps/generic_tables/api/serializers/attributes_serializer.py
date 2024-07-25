from rest_framework import serializers

from apps.generic_tables.models import *

class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)

    def to_representation(self, instance):
        return{ 
            'id' : instance.id,
            'name' : instance.name,
            'parameter_id' : instance.parameter.id,
            'parameter_name' : instance.parameter.name,
        }