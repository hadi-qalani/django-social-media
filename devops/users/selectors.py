from .models import Profile, BaseUser
from django.core.cache import cache

def get_profile(user:BaseUser) -> Profile:
    return Profile.objects.get(user=user)



def get_cache_profile(user:BaseUser) -> dict | None:
    return cache.get(f"profile_{user}")