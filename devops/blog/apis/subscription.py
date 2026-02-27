from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from devops.blog.models import Subscription
from django.core.paginator import Paginator
from drf_spectacular.utils import extend_schema


from devops.blog.services.post  import unsubscribe, subscribe

from devops.blog.selectors.get_subscribers  import get_subscribers




class SubscrbeDeleteAPI(APIView):
    #permission_classes = [IsAuthenticated]

    def delete(self, request, username):
        try:
            unsubscribe (user = request.user, username=username)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        return Response({"message": f"Unsubscribed from {username}"}, status=status.HTTP_204_NO_CONTENT)

    
class SubscribeAPI(APIView):
    #permission_classes = [IsAuthenticated]

    class InputSubSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=150)
    
    class OutputSubSerializer(serializers.ModelSerializer):
        class Meta:
            model = Subscription
            fields = ['subescriber', 'target']

    
    @extend_schema( responses=OutputSubSerializer,)
    def get(self, request):
        
        query = get_subscribers (user = request.user)

        paginator = Paginator(query, 10)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        serializer = self.OutputSubSerializer(page_obj.object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @extend_schema( request=InputSubSerializer,)
    def post(self, request):

        serializer = self.InputSubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = subscribe (user = request.user, username = serializer.validated_data['email'] )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": f"Subscribed to {serializer.validated_data['email']}"}, status=status.HTTP_201_CREATED)