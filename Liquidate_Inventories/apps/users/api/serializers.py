from rest_framework import serializers
from apps.users.models import CustomUser,Role

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def create(self,validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self,instance,validated_data):
        user_update = super().update(instance,validated_data)
        user_update.set_password(validated_data['password'])
        user_update.save()
        return user_update
class CustomUserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
            'last_name': instance['last_name'],
            'email': instance['email'],
            'password': instance['password'],
            'role': instance['role'],
        }
        
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