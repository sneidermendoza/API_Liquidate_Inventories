from rest_framework import serializers
from apps.users.models import Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        
class RoleListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Role
        fields = '__all__'
        
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'role': instance['name'],
        }
        
class UpdateRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('id','name')