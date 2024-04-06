from rest_framework import serializers

from apps.generic_tables.models import Menus

class MenuSerializer(serializers.ModelSerializer):
    option_name = serializers.CharField(source='option.name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = Menus
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',)