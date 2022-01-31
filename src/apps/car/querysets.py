from django.db.models import Avg, Count, QuerySet
from django.db.models.functions import Coalesce


class CarQuerySet(QuerySet):
    def with_avg_rating(self):
        return self.annotate(avg_rating=Coalesce(Avg("rates__rating"), 0.0))

    def by_most_popular(self):
        return self.annotate(rates_number=Count("rates")).order_by("-rates_number")
