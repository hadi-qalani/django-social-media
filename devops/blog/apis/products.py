from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework import serializers
from devops.blog.models import product
from devops.api.pagination import LimitOffsetPagination

from devops.blog.services.products import create_product
from devops.blog.selectors.products import get_products

from drf_spectacular.utils import extend_schema

class ProductApi(APIView):

    class pagination(LimitOffsetPagination):
        default_limit = 10
    

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)

    
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = product
            fields = ['name', 'created_at', 'updated_at']
            
    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #business logic method
        try:
            query = create_product(name=serializer.validated_data.get('name'))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        output_serializer = self.OutputSerializer(query)
        return Response({'data': output_serializer.data}, status=status.HTTP_201_CREATED)

    
    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        
        query = get_products()
        serializer = self.OutputSerializer(query, many=True)
        
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)