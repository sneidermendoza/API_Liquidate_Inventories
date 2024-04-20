from rest_framework import serializers
from apps.users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.generic_tables.models import Menus

class CustomTokenOptainPairSerializer(TokenObtainPairSerializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    # Define el campo adicional para los menús
    menus = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        exclude = ( 'is_staff', 'created_at', 'status','is_superuser','last_login','password','groups','user_permissions')

    def get_menus(self, instance):
        # Obtén el rol del usuario
        user_role = instance.role

        # Si el usuario no tiene un rol, devolver una lista vacía de menús
        if not user_role:
            return []

        # Obtén todos los menús asociados al rol del usuario
        menus = Menus.objects.filter(role=user_role)

        # Serializa los menús y devuelve la representación
        menus_data = []
        for menu in menus:
            menus_data.append({
                'id': menu.id,
                'option': menu.option.name,
                'link': menu.option.link,
            })

        return menus_data

    def to_representation(self, instance):
        # Serializa el usuario y sus menús
        representation = super().to_representation(instance)
        representation['menus'] = self.get_menus(instance)
        return representation
        
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