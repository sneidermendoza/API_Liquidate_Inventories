from rest_framework.response import Response
from rest_framework import status

def api_response(serializer_data, message=None, status_code=status.HTTP_200_OK):
    response = Response({'message': message,
                         'data': serializer_data,
                         'status' : status_code},
                        status=status_code)
    return response
