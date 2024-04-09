from rest_framework import serializers
from apps.business.models import Business
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'
        
    def to_representation(self, instance):
        return {
            'id' : instance.id,
            'user_id' : instance.user_id,
            'user_name' : instance.user.name,
            'name_business' : instance.name_business,
        }
        
class UpdateBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ('user','name_business')