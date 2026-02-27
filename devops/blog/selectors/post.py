from devops.users.models import BaseUser
from devops.blog.models import Subscription, Post
from django.db.models import QuerySet
from devops.blog.filters import PostFilter



def post_list(*, filters: dict = None, user: BaseUser, self_included: bool = True) -> QuerySet[Post]:
    filters = filters or {}
    
    my_followings = Subscription.objects.filter(subscriber=user)
    
    author_ids = list(my_followings.values_list("target", flat=True))
    
    if self_included:
        author_ids.append(user.id)
    
    if not author_ids:
        return Post.objects.none()
    
    query = Post.objects.filter(author__in=author_ids)
    filtered_query = PostFilter(filters, queryset=query).qs
    
    return filtered_query
    


def post_detail(*, slug:str, user:BaseUser) -> Post:
    subscription = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))

    try:
        post = Post.objects.get(slug=slug, author__in=subscription + [user.id]).val
    except Post.DoesNotExist:
        raise ValueError("Post not found")
    if post.author.id not in subscription and post.author != user:
        raise ValueError("You don't have permission to view this post")
    return post