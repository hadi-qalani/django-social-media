from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from devops.blog.models import Post
from django.core.paginator import Paginator
from devops.blog.models import Post
from django.urls import reverse

from devops.blog.services.post import  create_post
from devops.blog.selectors.post import post_list, post_detail

from drf_spectacular.utils import extend_schema


class PostApi (APIView):

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=50, required=False)
        search  = serializers.CharField(max_length=255, required=False)
        author__in = serializers.CharField(max_length=255, required=False)
        create_at__range = serializers.CharField(required=False)
        slug = serializers.CharField(max_length=100, required=False)
        content = serializers.CharField(max_length=1000, required=False)
        ...

    class InputPostSerializer(serializers.Serializer):
        content = serializers.CharField(max_length=1000)
        title = serializers.CharField(max_length=50)
        ...

    class OutputPostSerializer(serializers.ModelSerializer):
        url = serializers.SerializerMethodField("get_url")
        author = serializers.SerializerMethodField("get_author")
        
        def get_url(self, post) -> str | None:
            request = self.context.get('request')
            if request is not None:
                path = reverse("blog:post-detail", args=(post.slug,))
                return request.build_absolute_uri(path)
            return None

        
        def get_author(self, post) -> str | None:
            if post.author:
                return post.author.email
            return None


        class Meta:
            model = Post
            fields = ['slug', 'content', 'title', 'author', 'url']
        
        ...
    @extend_schema(responses=OutputPostSerializer)        
    def get(self, request):

        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            query = post_list (filters=filters_serializer.validated_data, user = request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        paginator = Paginator(query, 10)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serializer = self.OutputSerializer(page_obj.object_list, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

        ...
    @extend_schema(request=InputPostSerializer, responses=OutputPostSerializer)
    def post(self, request):

        serializer = self.InputPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            create_post (user=request.user, content = serializer.validated_data['content'], title = serializer.validated_data['title'])
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "post created successfully"}, status=status.HTTP_201_CREATED)
        ...

class PostDetailApi (APIView):

    class OutputDetailSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        
        def get_author(self, post) -> str | None:
            if post.author:
                return post.author.email
            return None

        class Meta:
            model = Post
            fields = ['slug', 'content', 'title', 'author']
        
    @extend_schema(responses=OutputDetailSerializer,)
    def get(self,request):
        query = post_detail(user=request.user, slug=request.query_params.get("slug"))

        serializer = self.OutputDetailSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
