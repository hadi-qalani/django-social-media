from devops.blog.models import product
from django.db.models import QuerySet


def get_products() -> QuerySet[product]:
    query = product.objects.all()
    return query

