from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from apps.users.api.serializers.user_serializer import *
from apps.helper.api_response_generic import api_response
from apps.users.models import CustomUser
from unidecode import unidecode
from django.db.models import Q

class CustomUserViewSet(viewsets.GenericViewSet):
    User = CustomUser
    serializer_class = CustomUserSerializer
    queryset = None
    
    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(status = True)
                            
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('-created_at'))
        search = self.request.query_params.get('search')
        if search:
            search_normalized = unidecode(search).lower()
            queryset = queryset.filter(
                Q(name__icontains=search_normalized)|
                Q(last_name__icontains=search)|
                Q(role__name__icontains=search)|
                Q(email__icontains=search)
                )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': serializer.data
            }
            return api_response(paginated_response, 'Usuarios Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            return api_response(serializer.data, 'Usuarios Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')
    
    def create(self, request):
        user_serializer= self.serializer_class(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return api_response(user_serializer.data,'Usuarios Creado Exitosamente!', status.HTTP_201_CREATED,None )
        return api_response([],None, status.HTTP_400_BAD_REQUEST,user_serializer.errors )
    
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return api_response(user_serializer.data,'Usuario Obtenido Exitosamente!',status.HTTP_200_OK,None)
    
    def update(self,request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateCustomUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return api_response(user_serializer.data,"Usuario Actualizado Correctamente",status.HTTP_200_OK,None)           
        return api_response([],None,status.HTTP_200_OK,user_serializer.errors)           

    def destroy(self, request, pk=None):
        user_destroy = self.User.objects.filter(id = pk).update(status= False)
        if user_destroy == 1:
            return api_response([], 'Usuario Eliminado Correctamente',status.HTTP_200_OK)
        return api_response([], 'El Usuario Que Desea Eliminar No Fue Encontrado',status.HTTP_404_NOT_FOUND)
    
    @action(detail = True, methods=['post'])
    def change_password(self,request,pk=None):
        user = self.get_object(pk)
        password_serializer = SetPasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return api_response([],'Contraseña Actualizada Con Exito',status.HTTP_200_OK)
        return api_response([],password_serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_user_business(self, request,pk=None):
        # Asumiendo que el ID 2 corresponde al rol de "cliente"
        client_role_id = 2
        clients = self.get_serializer().Meta.model.objects.filter(role__id=client_role_id, status=True)
        serializer = self.get_serializer(clients, many=True)
        if clients.exists():
            return api_response(serializer.data, 'Clientes Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        return api_response([], 'No se encontraron clientes', status.HTTP_404_NOT_FOUND, None)
    
