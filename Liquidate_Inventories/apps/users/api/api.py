from apps.users.models import CustomUser,Role
from apps.users.api.serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from apps.helper.api_response_generic import api_response

@api_view(['GET','POST'])
def custom_user_api_view(request):
    
    if request.method == 'GET':
        users = CustomUser.objects.all().values('id','name','last_name','email','password','role')
        users_serializer = CustomUserListSerializer(users, many=True)
        return api_response(users_serializer.data,'Usuarios obtenidos correctamente!',status.HTTP_200_OK)
    
    elif request.method == 'POST':  
        users_serializer = CustomUserSerializer(data = request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return api_response(users_serializer.data,'Usuarios creado correctamente!',status.HTTP_201_CREATED)
        return api_response([],users_serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','PUT','DELETE'])
def custom_user_detail_api_view(request,pk):
    
    user = CustomUser.objects.filter(id = pk).first()
    if user:
        if request.method == 'GET':
            user_serializer=CustomUserSerializer(user)
            return api_response(user_serializer.data,'Usuario obtenido correctamente!',status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            user_serializer=CustomUserSerializer(user, data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return api_response(user_serializer.data,'Usuario editado correctamente!',status.HTTP_200_OK)
            return api_response([],user_serializer.errors,status.HTTP_400_BAD_REQUEST)
             
        elif request.method == 'DELETE':
            user.delete()
            return api_response([],'usuario eliminado correctamente!',status.HTTP_200_OK)
    return api_response([],'No se ha encontrado un usuario con estos datos!',status.HTTP_404_NOT_FOUND)
        
@api_view(['GET','POST'])
def role_api_view(request):
    
    if request.method == 'GET':
        roles = Role.objects.all().values('id','name')
        role_serializer = RoleListSerializer(roles, many = True)
        return api_response(role_serializer.data,'Roles obtenidos correctamente!',status.HTTP_200_OK)
        
    elif request.method == 'POST':
        role_serializer = RoleSerializer(data = request.data)
        if role_serializer.is_valid():
            role_serializer.save()
            return api_response(role_serializer.data,'rol creado correctamente!',status.HTTP_201_CREATED)
        return api_response([],role_serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','PUT','DELETE'])
def role_detail_api_view(request,pk):
    
    role = Role.objects.filter(id =pk).first()
    if role:
        if request.method == 'GET':
            role_serializer=RoleListSerializer(role)
            return api_response(role_serializer.data,'Rol obtenido correctamente!',status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            role_serializer=RoleSerializer(role, data = request.data)
            if role_serializer.is_valid():
                role_serializer.save()
                return api_response(role_serializer.data,'Usuario editado correctamente!',status.HTTP_200_OK)
            return  api_response([],role_serializer.errors,status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            role.delete()
            return api_response([],'Rol eliminado correctamente!',status.HTTP_200_OK)
    return api_response([],'No se ha encontrado un rol con estos datos!',status.HTTP_404_NOT_FOUND)
        