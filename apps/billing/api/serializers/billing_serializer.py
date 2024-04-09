from rest_framework import serializers

from apps.billing.models import Billings

class BillinSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = Billings
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',)