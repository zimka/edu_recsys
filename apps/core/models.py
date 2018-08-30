from django.db import models
from django.utils import timezone

from apps.context.models import Student
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

    class Meta:
        abstract = True

    def __str__(self):
        return "{}/{}(({}): {}".format(self.user, self.item, self.created, self.score)

    @classmethod
    def create_from_raw(cls, raw):
        return cls.objects.create(**raw.to_kwargs())


class ImmutableMixin:
    """
    Примесь для изменяемых хранилищ
    """
    @classmethod
    def put_items(cls, recommendation_items):
        # TODO: bulk_create
        for r in recommendation_items:
            cls.create_from_raw(r)


class MutableMixin:
    """
    Примесь для неизменяемых хранилищ
    """
    @classmethod
    def put_items(cls, recommendation_items):
        """
        Метод работает линейно от количества итемов, но вызывается
        асинхронно, поэтому это нормально
        """
        for r in recommendation_items:
            updated = cls.objects.filter(user=r.user, item=r.item).update(**r.to_kwargs())
            if not updated:
                cls.objects.create(**r.to_kwargs())
