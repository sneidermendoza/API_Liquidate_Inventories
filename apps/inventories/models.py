from django.db import models
from simple_history.models import HistoricalRecords
from apps.bases_sms.models import BaseModel
from apps.business.models import Business
from apps.products.models import Products
from apps.generic_tables.models import Attributes

class Inventories(BaseModel):

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    inventory_status = models.ForeignKey(Attributes, on_delete=models.CASCADE)
    total_cost = models.DecimalField('Costo del Inventario', max_digits=20,decimal_places = 2, null = False)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    
    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return f"{self.business} - {self.total_cost}"
    
    
class InventoryDetails(BaseModel):
    
    inventory = models.ForeignKey(Inventories, on_delete=models.CASCADE)
    product =  models.ForeignKey(Products, on_delete=models.CASCADE)
    amount =  models.PositiveIntegerField("Cantidad del producto", null = False)
    is_valid = models.BooleanField(default=True)
    historical = HistoricalRecords()
    total_in_money =  models.PositiveIntegerField("total en dinero, calculodo multiplicando la cantidad del producto por el valor del producto", null = True)
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
    
    
    class Meta:
        verbose_name = 'Detalle de Inventario'
        verbose_name_plural = 'Detalle de Inventarios'

    def __str__(self):
        return f"{self.inventory} - {self.product} - {self.amount}"