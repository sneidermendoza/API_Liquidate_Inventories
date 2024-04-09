from rest_framework import serializers

from apps.generic_tables.models import *

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)        
