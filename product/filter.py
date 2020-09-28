from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from rest_framework.filters import OrderingFilter


class CistomOrdering(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            if any('rating_avg' in o for o in ordering):
                queryset = queryset.annotate(
                    rating_avg=Coalesce(Avg('rates__rate'),0)
                )
            if any('rating_count' in o for o in ordering):
                queryset = queryset.annotate(
                    rating_count=Count('rates')

                )
            return queryset.order_by(*ordering)
        return queryset