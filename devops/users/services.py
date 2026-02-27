from django.db import transaction 
from .models import BaseUser, Profile
from django.core.cache import cache


def create_profile(*, user:BaseUser, bio:str | None) -> Profile:
    return Profile.objects.create(user=user, bio=bio)

def create_user(*, email:str, password:str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password)


@transaction.atomic
def register(*, bio:str|None, email:str, password:str) -> BaseUser:

    user = create_user(email=email, password=password)
    create_profile(user=user, bio=bio)

    return user

def profile_count_update ():
    
    keys = cache.keys('profile_*')
    for key in keys:
        data = cache.get(key)
        email = key.replace("profile_", "")
        try:
            profile = Profile.objects.get(user__email=email)
            profile.posts_count        = data['posts_count']             #or data.get("posts_count")
            profile.subscriber_count   = data['subscriber_count']         #or data.get("followers_count")
            profile.subscription_count = data['subscription_count']        #or data.get("followings_count")
            profile.save()

        except Exception as e:
            print(f"Error getting profile for email {email}: {e}")
            continue
