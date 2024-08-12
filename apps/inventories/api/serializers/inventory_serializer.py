from rest_framework import serializers
from apps.inventories.models import   Inventories

class  InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventories
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)
        
    def to_representation(self, instance):
        print(instance)
        return {
            'id' : instance.id,
            'business' : instance.business_id,
            'business_name' : instance.business.name_business,
            'total_cost' : instance.total_cost,
            'inventory_status': instance.inventory_status_id,
            'inventory_status_name': instance.inventory_status.name
        }
        
class UpdateInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventories
        fields = ('business','total_cost', 'inventory_status')
    
    