from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.api.serializers.user_serializer import CustomTokenOptainPairSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from apps.helper.api_response_generic import api_response
from apps.users.models import CustomUser

class Login(TokenObtainPairView):
    serializer_class = CustomTokenOptainPairSerializer
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(
            email=email,
            password=password
        )
        
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response({
                    'token' : login_serializer.validated_data.get('access'),
                    'refresh-token' : login_serializer.validated_data.get('refresh'),
                    'user' : user_serializer.data,
                    'message': 'Inicio de Sesion Exitoso!'
                },status=status.HTTP_200_OK)
            return  api_response([],'Email o Contraseña Incorrecto', status.HTTP_400_BAD_REQUEST)
        return  api_response([],'Email o Contraseña Incorrecto', status.HTTP_400_BAD_REQUEST)
    

class Logout(GenericAPIView):
    serializer_class = CustomTokenOptainPairSerializer

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(id=request.data.get('user', 0))
        if user.exists:
            RefreshToken.for_user(user.first())
            return  api_response([],'Sesion Cerrada Correctamente', status.HTTP_200_OK)
        return  api_response([],'No Existe Este Usuario', status.HTTP_400_BAD_REQUEST)
