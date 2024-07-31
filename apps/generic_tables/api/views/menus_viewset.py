from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from apps.generic_tables.api.serializers.menus_serializer import MenuSerializer
from apps.generic_tables.models import Menus
from apps.helper.api_response_generic import api_response
from rest_framework import status



class MenuViewSet(viewsets.GenericViewSet):
    serializer_class = MenuSerializer
    Menu = Menus
    queryset = None
    
    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
                            
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('-created_date'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            menu_serializer = self.get_serializer(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': menu_serializer.data
            }
            return api_response(paginated_response, 'Menus Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        menu_serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            return api_response(menu_serializer.data, 'Menus Obtenidos Exitosamente!', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')
    
    
    def create(self, request):
        menu_serializer= self.serializer_class(data = request.data)
        if menu_serializer.is_valid():
            menu_serializer.save()
            return api_response(menu_serializer.data,'Menu Creado Exitosamente!', status.HTTP_201_CREATED ,None)
        return api_response([],None, status.HTTP_400_BAD_REQUEST,menu_serializer.errors )
    
    def retrieve(self, request, pk=None):
        menu = self.get_object(pk)
        menu_serializer = self.serializer_class(menu)
        return api_response(menu_serializer.data,'Menu Obtenido Exitosamente!',status.HTTP_200_OK,None)
    
    def update(self,request, pk=None):
        menu = self.get_object(pk)
        menu_serializer = self.serializer_class(menu, data=request.data)
        if menu_serializer.is_valid():
            menu_serializer.save()
            return api_response(menu_serializer.data,"Menu Actualizado Correctamente",status.HTTP_200_OK,None)           
        return api_response([],None,status.HTTP_200_OK,menu_serializer.errors)           


    def destroy(self, request, pk=None):
        menu_destroy = self.Menu.objects.filter(id = pk).update(state= False)
        if menu_destroy == 1:
            return api_response([], 'Menu Eliminado Correctamente',status.HTTP_200_OK,None)
        return api_response([], None,status.HTTP_404_NOT_FOUND,'El Menu Que Desea Eliminar No Fue Encontrado')
    