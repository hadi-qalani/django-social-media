import profile

from django.db.transaction import atomic
from django.db.models import QuerySet

from devops.blog.models import Post, Subscription
from devops.users.models import BaseUser

from django.utils.text import slugify
from django.core.cache import cache


    


def count_posts(*,user:BaseUser) -> int:
    return  Post.objects.filter(author = user).count()
   

def count_follower(*,user:BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()
    

def count_following(*,user:BaseUser) -> int:
    return Subscription.objects.filter(subescriber=user).count()
    

# with HMSET(f"profile_{user}", {"posts_count": count_posts(user=user), "follower_count": count_follower(user=user), "following_count": count_following(user=user)})
# cache.HINCRBY(f"profile_{user}", "posts_count", 1) # for incrementing posts count by 1 can write atomic code and prevent racecondition
def cache_profile(user:BaseUser) -> None:
    profile = user.profile
    cache.set(
        f"profile_{user}",
        {
        "bio": profile.bio,
        "posts_count" :count_posts(user=user),
        "subscriber_count" :count_follower(user=user),
        "subscription_count" :count_following(user=user),
        },
        timeout=None)


def subscribe(*, user:object, username:str) -> QuerySet:
    target = BaseUser.objects.get(email=username)
    if target == user:
        raise ValueError("You cannot subscribe to yourself")
    sub = Subscription.objects.create(subscriber=user, target=target)

    sub.full_clean()
    sub.save()

    cache_profile(user=user)

    return sub




def unsubscribe(*, user:BaseUser, username:str) -> None:
    target = BaseUser.objects.get(email=username)
    if target == user:
        raise ValueError("You cannot unsubscribe from yourself")
    Subscription.objects.filter(subscriber=user, target=target).delete()

    cache_profile(user=user)

    return None
    

@atomic
def create_post(*, title:str, content:str, user:BaseUser) -> object:
    post = Post.objects.create(title=title, content=content, author=user, slug=(slugify(title)))

    cache_profile(user=user)

    return post