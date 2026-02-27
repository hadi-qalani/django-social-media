
from devops.users.models import BaseUser
from devops.blog.models import Subscription, Post
from django.db.models import QuerySet
from devops.blog.filters import PostFilter



def get_subscribers (*, user:BaseUser) -> QuerySet[Subscription]:
    query = Subscription.objects.filter(target = user).select_related("subscriber")
    return query


