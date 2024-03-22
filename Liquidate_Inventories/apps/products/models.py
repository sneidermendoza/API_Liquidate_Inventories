from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.generic_tables.models import MeasureUnits


class Products(BaseModel):
    
    code = models.IntegerField(("Codigo del Producto"), null = True )
    name = models.CharField('Nombre del producto', max_length= 150, null = False, unique = True)
    description = models.CharField('Descripcion', max_length= 250, null = True)
    price = models.DecimalField(("Precio del Producto"), max_digits=20,decimal_places=2)
    measure_units = models.ForeignKey(MeasureUnits, on_delete=models.CASCADE)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
    
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.code,self.name,self.description,self.price