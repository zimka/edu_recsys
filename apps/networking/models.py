from uuid import uuid4
from apps.context.models import Student
from model_utils.fields import AutoLastModifiedField
from django.db import models
from jsonfield import JSONField
from apps.core.models import MutableMixin, AbstractRecommendation


class NetworkingRecommendationDeprecated(models.Model):
    # TODO: это временная имплементация для ВЭФ
    # Рекомендации различного типа должны быть либо разделены, либо
    # храниться как отдельные поля
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(Student, on_delete=models.PROTECT)
    recommendations = JSONField()
    created = AutoLastModifiedField()


class NetworkingRecommendation(MutableMixin, AbstractRecommendation):
    COMPETENCE = "cmp"
    INTEREST = "int"
    EXPERIENCE = "exp"
    TYPE_CHOICES = (
        (COMPETENCE, "competence"),
        (INTEREST, "interest"),
        (EXPERIENCE, "experience")
    )

    class Meta:
        unique_together = ("user", "type")
    item = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
