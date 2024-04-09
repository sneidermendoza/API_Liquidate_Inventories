from rest_framework import serializers
from apps.products.models import  Products

class  ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)
        
    def to_representation(self, instance):
        return {
            'id' : instance.id,
            'code' : instance.code,
            'name' : instance.name,
            'description' : instance.description,
            'measure_units' : instance.measure_units.id,
            'measure_units_name' : instance.measure_units.name,
            'price' : instance.price,
        }
    