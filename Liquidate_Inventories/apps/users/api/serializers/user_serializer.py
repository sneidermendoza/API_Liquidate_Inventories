from rest_framework import serializers
from apps.users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenOptainPairSerializer(TokenObtainPairSerializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('state', 'created_date', 'modified_date','deleted_date',)

    def to_representation(self, instance):
        return{ 
            'id' : instance.id,
            'name' : instance.name,
            'last_name' : instance.last_name,
            'email' : instance.email,
            'role_id' : instance.role_id,
            'role_name' : instance.role.name,
        }
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def to_representation(self, instance):
        return {
           'id' : instance.id,
            'name' : instance.name,
            'last_name' : instance.last_name,
            'email' : instance.email,
            'role_id' : instance.role_id,
            'role_name' : instance.role.name,
        }
        
        
    
    def create(self,validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UpdateCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name','last_name','role', 'email')
    
class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=120, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=120, min_length=6, write_only=True)
    
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
                )
        return data