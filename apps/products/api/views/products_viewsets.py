from rest_framework import status
from rest_framework import viewsets
from apps.products.api.serializers.products_serializer import ProductSerializer
from apps.helper.api_response_generic import  api_response



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk,state = True).first()
        
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': serializer.data
            }
            return api_response(paginated_response, 'Lista de productos', status.HTTP_200_OK, None)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return api_response(serializer.data, 'Lista de productos', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')

    def create(self,request):
        serializer_data = self.serializer_class(data = request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return api_response(serializer_data.data, 'Producto Creado con exito!',status.HTTP_201_CREATED , None)
              
    def destroy(self, request, pk=None):
        product = self.get_queryset().filter(id = pk).first()
        if product:
            product.state = False
            product.save()
            return api_response([],'Producto eliminado con exito!', status.HTTP_200_OK, None)
        return api_response([],None, status.HTTP_404_NOT_FOUND,'No se encontro el registro')
    
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return api_response(product_serializer.data,'Producto actualizado!', status.HTTP_200_OK, None)
            return api_response([], None,status.HTTP_404_NOT_FOUND,product_serializer.errors)
    