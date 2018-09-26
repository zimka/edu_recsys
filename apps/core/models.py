from django.db import models
from django.db import transaction
from django.utils import timezone
from simple_history.models import HistoricalRecords

from edu_coresys.models import Student
from apps.core.raw_recommendation import RawRecommendation


class AbstractRecommendation(models.Model, RawRecommendation):
    """
    Хранилище рекомендаций. Можно сохранять "сырые" рекомендации
    """
    user = models.ForeignKey(Student, on_delete=models.PROTECT)
    item = None
    score = models.FloatField()
    source = models.CharField(max_length=255)

    created = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords(inherit=True)

    # Нужно ли при записи рекомендаций юзера удалять все
    # его старые рекомендации
    CLEAR_UPDATE_USERS = False

    class Meta:
        abstract = True

    def __str__(self):
        return "{}/{}((): {}".format(self.user, self.item, self.score)

    @classmethod
    def put_single(cls, raw, options={}):
        now = timezone.now()

        if not raw.created:
            raw.created = now
        data = raw.to_kwargs()
        if options:
            data.update(options)
        obj, created = cls.objects.update_or_create(defaults=data, item=raw.item, user=raw.user)
        return obj, created

    @classmethod
    def put_many(cls, raw_list, options={}):
        """
        Метод работает линейно от количества итемов, но вызывается
        асинхронно, поэтому это нормально
        """
        now = timezone.now()

        with transaction.atomic():
            if cls.CLEAR_UPDATE_USERS:
                update_users = set(r.user for r in raw_list)
                cls.objects.filter(user__in=update_users).delete()

            for r in raw_list:
                if not r.created:
                    r.created = now
                cls.put_single(r, **options)
