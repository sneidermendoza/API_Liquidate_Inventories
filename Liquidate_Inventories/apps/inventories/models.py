from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.business.models import Business
from apps.products.models import Products

class Inventories(BaseModel):

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
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
        return self.name
    
    
class InventoryDetails(BaseModel):
    
    inventory = models.ForeignKey(Inventories, on_delete=models.CASCADE)
    product =  models.ForeignKey(Products, on_delete=models.CASCADE)
    amount =  models.IntegerField("Cantidad del producto", null = False)
    historical = HistoricalRecords()
    
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
        return self.inventory,self.product