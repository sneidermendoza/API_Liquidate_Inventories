from django.urls import path
from apps.generic_tables.api.views.general_views import *

urlpatterns = [
    path('measure_units/', MeasureUnitsListAPIView.as_view(), name= 'Unidad de Medida'),
    path('parameter/', ParameterListAPIView.as_view(), name= 'Parametros'),
    path('attributes/', AttributesListAPIView.as_view(), name= 'Atributos'),
]
