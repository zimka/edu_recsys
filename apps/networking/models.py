from uuid import uuid4
from apps.context.models import Student
from model_utils.fields import AutoLastModifiedField
from django.db import models
from django.conf import settings
from jsonfield import JSONField
from .compute import get_networking_json


class NetworkingRecommendation(models.Model):
    # TODO: это временная имплементация для ВЭФ
    # Рекомендации различного типа должны быть либо разделены, либо
    # храниться как отдельные поля
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(Student, on_delete=models.PROTECT)
    recommendations = JSONField()
    created = AutoLastModifiedField()
