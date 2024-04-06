from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from apps.users.models import Role

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
    description = models.CharField('descripcion', max_length= 50, null = False, unique = True)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    
    class Meta:
        verbose_name = 'Parametro'
        verbose_name_plural = 'Parametros'

    def __str__(self):
        return f"{self.name} - {self.description}"

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
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'

    def __str__(self):
        return self.name
    
class Options(BaseModel):

    name = models.CharField('nombre', max_length= 50, null = False, unique = True)
    description = models.CharField('descripcion', max_length=50,null = True)
    link = models.CharField('link', max_length=50, null = True)
    icon = models.CharField('icono', max_length=50 , blank=True)
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    
    class Meta:
        verbose_name = 'Opcion'
        verbose_name_plural = 'Opciones'

    def __str__(self):
        return self.name
    
class Menus(BaseModel):

    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    
    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu'

    def __str__(self):
        return self.option.name
    
