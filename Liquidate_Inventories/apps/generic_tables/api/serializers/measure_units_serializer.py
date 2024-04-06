from rest_framework import serializers

from apps.generic_tables.models import *

class MeasureUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnits
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)
    