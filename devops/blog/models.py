from django.db import models
from devops.common.models import BaseModel
from devops.users.models import BaseUser
from django.core.exceptions import ValidationError
class product(BaseModel):
    name = models.CharField(max_length=255)
    

class Post(models.Model):
    slug = models.SlugField(primary_key=True, max_length=100)
    title = models.CharField(max_length=50, unique=True)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)

class Subscription (models.Model):
    subescriber = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="subs")
    target = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="targets")

    def clean(self):
        if self.subescriber == self.target:
            raise ValidationError("subscriber can not be equal to target")
    
    def __str__(self):

        return f"{self.subescriber.email} is subscribed to {self.target.email}"