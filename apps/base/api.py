from rest_framework import generics
from apps.helper.api_response_generic import api_response

class GeneralListAPIview(generics.ListAPIView):
    serializer_class = None
    
    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(state = True)