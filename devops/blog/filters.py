from django_filters import FilterSet, CharFilter
from django.utils import timezone
from devops.blog.models import Post
from datetime import datetime
from django.contrib.postgres.search import SearchVector


class PostFilter(FilterSet):
    search = CharFilter(method='filter_search')
    author__in = CharFilter(method='filter_author__in')
    created_at__range = CharFilter(method='filter_created_at__range')

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector('title', 'content')).filter(search=value)
        ...

    def filter_author__in(self, queryset, name, value):
        authors= value.split(",")
        return queryset.filter(author__username__in=authors)
        

    # def filter_created_at__range(self, queryset, name, value):
    #     dates = value.split(",")
    #     limit =  2
    #     if len(dates) > 2:
    #         raise ValueError("Invalid date range format. Expected format: 'start_date,end_date'")       
        
    #     created_at_0 , created_at_1 = dates
    #     if not created_at_0:
    #         return queryset.filter(created_at__date__lte=created_at_1)
    #     if not created_at_1:
    #         return queryset.filter(created_at__date__gte=created_at_0)
    #     return queryset.filter(created_at__date__range = (created_at_0, created_at_1)   )

    def filter_created_at__range(self, queryset, name, value):
        dates = value.split(",")

        if len(dates) > 2:
            raise ValueError(
                "Invalid date range format. Expected format: 'start_date,end_date'"
            )

        if len(dates) == 1:
            dates.append("")

        created_at_0, created_at_1 = dates

        if created_at_0:
            created_at_0 = datetime.strptime(created_at_0.strip(), "%Y-%m-%d")

        if created_at_1:
            created_at_1 = datetime.strptime(created_at_1.strip(), "%Y-%m-%d")

        if created_at_0 and created_at_1:
            return queryset.filter(created_at__range=(created_at_0, created_at_1))

        if created_at_0:
            return queryset.filter(created_at__gte=created_at_0)

        if created_at_1:
            return queryset.filter(created_at__lte=created_at_1)

        return queryset



    class Meta:
        fields = ['title', 'slug']
        model = Post