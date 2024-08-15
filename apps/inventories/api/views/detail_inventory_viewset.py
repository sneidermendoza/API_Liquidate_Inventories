from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.inventories.api.serializers.detail_inventory_serializer import InventoryDetailSerializer, InventoryDetailListSerializer
from apps.inventories.models import InventoryDetails, Inventories
from apps.helper.api_response_generic import api_response
from apps.billing.models import Billings
from unidecode import unidecode
from django.db.models import Q
from apps.enum.enum_general import INVENTORY_STATUS_FINALIZED, PENDING_BILLING_STATUS

class InventoryDetailsViewSet(viewsets.GenericViewSet):
    DetailInventory = InventoryDetails
    serializer_class = InventoryDetailSerializer
    
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)
    
    def create(self, request):
        
        inventory_id = request.data[0]['inventory']
        # Verificar si ya existen detalles de inventario para el inventory_id proporcionado
        if self.DetailInventory.objects.filter(inventory_id=inventory_id).exists():
            return api_response([], None, status.HTTP_400_BAD_REQUEST, f'El inventario con ID {inventory_id} ya tiene detalles registrados en la base de datos.')
        
        detail_serializer = self.serializer_class(data=request.data, many=True)
        if detail_serializer.is_valid():
            details = detail_serializer.validated_data
            inventory_details = [self.DetailInventory(**detail) for detail in details]
            self.DetailInventory.objects.bulk_create(inventory_details)
        
            # Calcular el costo total del inventario
            inventory_id = request.data[0]['inventory']  # Suponiendo que el id del inventario está en el primer detalle
            total_cost = 0
            for detail in details:
                product = detail['product']
                quantity = detail['amount']
                product_price = product.price  # Obtener el precio del producto del objeto
                total_cost += float(product_price) * quantity  # Asegúrate de que product_price sea un número
        
            try:
                # Actualizar el costo del inventario
                inventory = Inventories.objects.get(id=inventory_id)
                inventory.total_cost = total_cost
                inventory.inventory_status_id = INVENTORY_STATUS_FINALIZED
                inventory.save()
                
                # Crear el registro en la tabla de facturacion
                total_profit = total_cost * 0.02 
                billing = Billings.objects.create(
                    inventory=inventory,
                    attribute_id = PENDING_BILLING_STATUS,
                    total_profit=total_profit
                )
            except Inventories.DoesNotExist:
                return api_response([], None, status.HTTP_404_NOT_FOUND,'El Parametro Que Desea Eliminar No Fue Encontrado')
        
            return api_response(detail_serializer.data, 'Detalles del Inventario Creado con Éxito', status.HTTP_201_CREATED,None)
        else:
            return api_response([], None, status.HTTP_400_BAD_REQUEST,detail_serializer.errors)
        
    def list(self, request):
        business_id = request.query_params.get('business_id')
        queryset = self.DetailInventory.objects.filter(inventory__business_id=business_id, state=True).order_by('-created_date')
        page = self.paginate_queryset(queryset)
        search = self.request.query_params.get('search')
        if search:
            search_normalized = unidecode(search).lower()
            queryset = queryset.filter(
                Q(business__name__icontains=search_normalized)|
                Q(product__name__icontains=search)
                )
        if page is not None:
            serializer = InventoryDetailListSerializer(page, many=True)
            paginated_response = {
                'count': self.paginator.page.paginator.count,
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'results': serializer.data
            }
            return api_response(paginated_response, 'Registros Obtenidos con Éxito', status.HTTP_200_OK, None)
        if queryset.exists():
            serializer = InventoryDetailListSerializer(queryset, many=True)
            return api_response(serializer.data, 'Registros Obtenidos con Éxito', status.HTTP_200_OK, None)
        return api_response([], None, status.HTTP_404_NOT_FOUND, 'No se encontraron registros')

    def retrieve(self, request, pk=None):
        queryset = self.DetailInventory.objects.filter(inventory_id=pk, state=True)
        if not queryset.exists():
            return api_response([], None, status.HTTP_404_NOT_FOUND,'No se encontraron registros para el ID de inventario proporcionado')
        serializer = InventoryDetailListSerializer(queryset, many=True)
        return api_response(serializer.data, 'Registros de Detalle de Inventario Obtenidos con Éxito', status.HTTP_200_OK,None)
    
    def update(self, request, pk=None):
        # Obtener el ID del inventario desde los parámetros de la solicitud
        inventory_id = pk

        # Obtener los datos enviados en la solicitud
        data = request.data

        # Crear un diccionario para almacenar los detalles de respuesta
        response_details = []

        # Iterar sobre los datos recibidos para actualizar los registros correspondientes
        for item in data:
            # Obtener el ID del registro a actualizar
            detail_id = item.get('id')
        
            try:
                # Obtener el registro a actualizar
                detail_instance = self.DetailInventory.objects.get(id=detail_id, inventory_id=inventory_id)

                # Actualizar los campos del registro con los datos enviados
                detail_instance.amount = item.get('amount')  # Actualizar el campo 'amount'
                detail_instance.product_id = item.get('product_id')  # Actualizar el campo 'product_id'
                detail_instance.save()

                # Serializar el detalle actualizado y agregarlo a la respuesta
                detail_serializer = self.serializer_class(detail_instance)
                response_details.append(detail_serializer.data)
            except self.DetailInventory.DoesNotExist:
                # Si el registro no existe, agregar un mensaje de error al detalle de respuesta
                response_details.append({'error': f'Registro con ID {detail_id} no encontrado para el inventario con ID {inventory_id}'})

        # Devolver la respuesta con los detalles actualizados
        return api_response(response_details, 'Detalles de inventario actualizados con éxito', status.HTTP_200_OK,None)
    
    def destroy(self, request, pk=None):
        # Obtener el ID del inventario desde los parámetros de la solicitud
        inventory_id = pk

        # Obtener los datos enviados en la solicitud
        data = request.data

        # Verificar si se enviaron datos en el body de la solicitud
        if data:
            # Se enviaron datos en el body, lo que significa que se deben editar registros específicos
            # Iterar sobre los datos recibidos para actualizar los registros correspondientes
            for item in data:
                # Obtener el ID del registro a eliminar
                detail_id = item.get('id')
            
                try:
                    # Obtener el registro a eliminar
                    detail_instance = self.DetailInventory.objects.get(id=detail_id, inventory_id=inventory_id)

                    # Cambiar el estado del registro a inactivo (eliminar lógicamente)
                    detail_instance.state = False
                    detail_instance.save()
                except self.DetailInventory.DoesNotExist:
                    # Si el registro no existe, continuar con el siguiente
                    pass

            return api_response([], 'Registros eliminados con éxito', status.HTTP_200_OK,None)
        else:
            # No se enviaron datos en el body, lo que significa que se deben eliminar todos los registros del inventario
            try:
                # Obtener todos los registros del inventario especificado
                queryset = self.DetailInventory.objects.filter(inventory_id=inventory_id)

                # Cambiar el estado de todos los registros a inactivo (eliminar lógicamente)
                queryset.update(state=False)

                return api_response([], 'Todos los registros del inventario eliminados con éxito', status.HTTP_200_OK,None)
            except self.DetailInventory.DoesNotExist:
                return api_response([], None, status.HTTP_404_NOT_FOUND,'No se encontraron registros para el ID de inventario proporcionado')
