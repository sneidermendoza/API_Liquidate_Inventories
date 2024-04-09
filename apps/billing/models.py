from django.db import models
from simple_history.models import HistoricalRecords
from apps.bases_sms.models import BaseModel
from apps.generic_tables.models import Attributes
from apps.inventories.models import Inventories

class Billings(BaseModel):

    inventory = models.ForeignKey(Inventories, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)
    total_profit = models.PositiveIntegerField('Total Ganancia', null = False)
    historical = HistoricalRecords()
    
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value
        
    
    class Meta:
        verbose_name = 'Facturacion'
        verbose_name_plural = 'Facturacion'

    def __str__(self):
        return f"{self.inventory} - {self.attribute} - {self.total_profit}"
    