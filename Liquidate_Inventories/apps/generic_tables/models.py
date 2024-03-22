from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel

class MeasureUnits(BaseModel):

    name = models.CharField('nombre', max_length= 50, null = False, unique = True)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    
    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medidas'

    def __str__(self):
        return self.name
    

class Parameter(BaseModel):

    name = models.CharField('nombre', max_length= 50, null = False, unique = True)
    descriptiom = models.CharField('descripcion', max_length= 50, null = False, unique = True)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    
    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medidas'

    def __str__(self):
        return self.name, self.descriptiom

class Attributes(BaseModel):

    name = models.CharField('nombre', max_length= 50, null = False, unique = True)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    
    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medidas'

    def __str__(self):
        return self.name
    
