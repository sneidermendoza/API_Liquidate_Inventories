from django.db import models
from apps.base.models import BaseModel
from apps.users.models import CustomUser

class Business(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_business = models.CharField(("Nombre del Negocio"), max_length=50, unique = True, null = False)
    

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    class Meta:
        verbose_name = 'Nombre del Negocio'

    def __str__(self):
        return self.total_profit