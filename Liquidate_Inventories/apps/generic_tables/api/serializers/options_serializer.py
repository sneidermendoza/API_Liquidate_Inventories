from rest_framework import serializers

from apps.generic_tables.models import Options

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)