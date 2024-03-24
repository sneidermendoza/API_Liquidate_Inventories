from apps.base.api import GeneralListAPIview
from apps.generic_tables.api.serializers.general_serializer import *


class MeasureUnitsListAPIView(GeneralListAPIview):
    serializer_class = MeasureUnitsSerializer
     
class ParameterListAPIView(GeneralListAPIview):
    serializer_class = parameterSerializer

class AttributesListAPIView(GeneralListAPIview):
    serializer_class = AttributesSerializer
      