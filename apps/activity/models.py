from datetime import datetime
import pytz

from django.db import models

from apps.context.models import Activity
from apps.core.models import AbstractRecommendation, MutableMixin, ImmutableMixin


class ActivityRecommendationFresh(MutableMixin, AbstractRecommendation):
    """
    Актуальные рекомендации активностей для юзера
    """
    item = models.ForeignKey(Activity, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("user", "item")

    @classmethod
    def get_fresh_queryset(cls, created_after=None):
        if created_after is None:
            created_after = datetime(1970, 1, 1, tzinfo=pytz.utc)
        qs = cls.objects.filter(created__gt=created_after)
        return qs


class ActivityRecommendationLogs(ImmutableMixin, AbstractRecommendation):
    """
    Все сгенерированные активности для юзера
    """
    item = models.ForeignKey(Activity, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("user", "item", "created")
