from rest_framework import serializers
from apps.inventories.models import InventoryDetails

class InventoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryDetails
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)

class InventoryDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryDetails
        fields = ['id', 'inventory', 'amount']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['business_id'] = instance.inventory.business.id
        representation['business_name'] = instance.inventory.business.name_business
        representation['product_id'] = instance.product.id
        representation['product_name'] = instance.product.name
        return representation