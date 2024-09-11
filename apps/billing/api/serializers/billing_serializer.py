from rest_framework import serializers
from apps.billing.models import Billings
from apps.inventories.models import Inventories
from apps.generic_tables.models import Attributes
from apps.business.models import Business  # Asegúrate de importar el modelo correspondiente a Business

class BillinSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    business_name = serializers.CharField(source='inventory.business.name_business', read_only=True)

    class Meta:
        model = Billings
        exclude = ('state', 'modified_date', 'deleted_date',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Puedes agregar más personalización aquí si lo necesitas
        return representation
