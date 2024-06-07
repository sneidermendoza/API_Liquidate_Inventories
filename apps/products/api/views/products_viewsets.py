from rest_framework import status
from rest_framework import viewsets
from apps.products.api.serializers.products_serializer import ProductSerializer
from apps.helper.api_response_generic import  api_response
from rest_framework.decorators import action
import pandas as pd
from apps.products.models import Products
from apps.generic_tables.models import MeasureUnits



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk,state = True).first()
        
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        if queryset.exists():
            return api_response(serializer.data,'Lista de productos',status.HTTP_200_OK, None)
        return api_response([],None,status.HTTP_404_NOT_FOUND,'No se encontraron registros')

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
        
    @action(detail=False, methods=['post'])
    def bulk_create_products_excel(self, request):
        # Verificar si se proporcionó un archivo Excel en la solicitud
        if 'excel_file' not in request.FILES:
            return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se proporcionó ningún archivo Excel.')

        excel_file = request.FILES['excel_file']
    
        columns_to_read = ['CODIGO', 'NOMBRE DEL PRODUCTO', 'DESCRIPCION', 'PRECIO', 'UNIDAD DE MEDIDA']
    
        # Lee el archivo Excel
        try:
            df = pd.read_excel(excel_file, usecols=columns_to_read)
        except Exception as e:
            return api_response([], None, status.HTTP_404_NOT_FOUND, f'Error al leer el archivo Excel: {str(e)}')

        # Elimina las filas con valores nulos en todas las columnas
        df = df.dropna(how='all')
        if df.empty:
            return api_response([], None, status.HTTP_404_NOT_FOUND, 'El archivo Excel está vacío.') 

        # Mapear las columnas del DataFrame a los campos del modelo Products
        column_mapping = {
            'CODIGO': 'code',
            'NOMBRE DEL PRODUCTO': 'name',
            'DESCRIPCION': 'description',
            'PRECIO': 'price',
            'UNIDAD DE MEDIDA': 'measure_units_id',  # Cambia 'measure_units' a 'measure_units_id'
        }
    
        # Filtrar solo las columnas del DataFrame que necesitas
        df_filtered = df[column_mapping.keys()]

        # Renombrar las columnas del DataFrame según el mapeo
        df_filtered = df_filtered.rename(columns=column_mapping)
    
        # Convertir el DataFrame en una lista de diccionarios
        products_data = df_filtered.to_dict('records')

        # Crear productos en la base de datos utilizando bulk_create
        for data in products_data:
            # Busca el objeto MeasureUnits correspondiente al ID proporcionado en el archivo Excel
            measure_units_id = data.pop('measure_units_id')
            try:
                measure_units = MeasureUnits.objects.get(id=measure_units_id)
            except MeasureUnits.DoesNotExist:
                # Maneja el caso en el que no se encuentra el objeto MeasureUnits
                # Por ejemplo:
                return api_response([], None, status.HTTP_404_NOT_FOUND, f'No se encontró una unidad de medida con el ID {measure_units_id}')
                pass
            else:
                data['measure_units'] = measure_units
        
        # Crear productos en la base de datos utilizando bulk_create
        products_created = Products.objects.bulk_create([Products(**data) for data in products_data])

        # Serializar los productos creados
        serializer = ProductSerializer(products_created, many=True)

        return api_response(serializer.data, 'Productos Creados con exito!', status.HTTP_200_OK, None)