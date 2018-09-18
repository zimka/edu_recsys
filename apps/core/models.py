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
    def create_from_raw(cls, raw, options=None):
        data = raw.to_kwargs()
        if options is not None:
            data.update(options)
        return cls.objects.create(**data)


class ImmutableMixin:
    """
    Примесь для изменяемых хранилищ
    """
    @classmethod
    def put_items(cls, recommendation_items, options=None):
        # TODO: bulk_create
        for r in recommendation_items:
            cls.create_from_raw(r, options)


class MutableMixin:
    """
    Примесь для неизменяемых хранилищ
    """
    @classmethod
    def put_items(cls, recommendation_items, options=None):
        """
        Метод работает линейно от количества итемов, но вызывается
        асинхронно, поэтому это нормально
        """
        for r in recommendation_items:
            data = r.to_kwargs()
            if options is not None:
                data.update(options)
            updated = cls.objects.filter(user=r.user, item=r.item).update(**data)
            if not updated:
                cls.objects.create(**data)
