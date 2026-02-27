from django.urls import path, include
from devops.blog.apis.products import ProductApi

from devops.blog.apis.post import PostApi, PostDetailApi
from devops.blog.apis.subscription import SubscribeAPI, SubscrbeDeleteAPI

urlpatterns = [
    path('product/', ProductApi.as_view(), name='product'),
    path('post/', PostApi.as_view(), name='post'),
    # path('post-detail/<slug:slug>/', PostDetailApi.as_view(), name='post-detail'),
    path('post-detail/', PostDetailApi.as_view(), name='post-detail'),
    path('subscription/', SubscribeAPI.as_view(), name='subscription'),
    path('unsubscribe/<str:username>/', SubscrbeDeleteAPI.as_view(), name='unsubscribe'),

    ]