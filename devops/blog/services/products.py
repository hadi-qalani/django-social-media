from devops.blog.models import product
from django.db.models import QuerySet


def create_product(name: str) -> QuerySet[product]:
    query = product.objects.create(name=name)
    return query
  