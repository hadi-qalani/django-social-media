from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_validator, letter_validator
from devops.users.models import BaseUser , Profile
from devops.api.mixins import ApiAuthMixin
from devops.users.selectors import get_profile, get_cache_profile
from devops.users.services import register 
from django.core.cache import cache

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated, BasePermission



class ProfileApi(ApiAuthMixin, APIView):
    #permission_classes = []
    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile 
            fields = ("bio", "posts_count", "subscriber_count", "subscription_count")
        
        #thereis another way to add cache data to response without adding them to model and serializer by overriding to_representation method of serializer and add cache data to response if exist but in this way we cannot use cache data in other places like profile update api and we have to get data from cache in that api too and add them to response but if we add cache data to model and serializer we can use them in all places without getting data from cache again and again
        # def to_representation(self, instance):
        #     rep = super().to_representation(instance)
        #     cache_profile = cache.get(f"profile_{instance.user}", {})
        #     if cache_profile:
        #         rep["posts_count"] = cache_profile.get("posts_count")
        #         rep["subscriber_count"] = cache_profile.get("subscribers_count")
        #         rep["subscription_count"] = cache_profile.get("subscriptions_count")

        #     return rep

    @extend_schema(responses=OutPutSerializer)
    def get(self, request):
        data = get_cache_profile(user=request.user)
        if data is not None:
            return Response(data, status=status.HTTP_200_OK)

        query = get_profile(user=request.user)
        return Response(self.OutPutSerializer(query, context={"request":request}).data, status=status.HTTP_200_OK)


class RegisterApi(APIView):


    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        bio = serializers.CharField(max_length=1000, required=False)
        password = serializers.CharField(
                validators=[
                        number_validator,
                        letter_validator,
                        special_char_validator,
                        MinLengthValidator(limit_value=10)
                    ]
                )
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("email Already Taken")
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data


    class OutPutRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser 
            fields = ("email", "token", "created_at", "updated_at")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data


    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                    email=serializer.validated_data.get("email"),
                    password=serializer.validated_data.get("password"),
                    bio=serializer.validated_data.get("bio"),
                    )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(self.OutPutRegisterSerializer(user, context={"request":request}).data)

