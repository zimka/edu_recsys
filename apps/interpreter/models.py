from uuid import uuid4
from django.db import models
from jsonfield import JSONField
from apps.context.models import Student
from .tasks import compute_single_score_async

class ComputeTask(models.Model):
    input = JSONField(default={})
    output = JSONField(default={})
    complete = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def compute(self):
        pass


class SingleScoreComputeTask(ComputeTask):
    uuid = models.UUIDField(default=uuid4(), primary_key=True)
    user = models.ForeignKey(Student, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.user)

    def compute_async(self):
        compute_single_score_async(self.uuid)

    def compute(self):
        pass

    def _fetch_input(self):
        pass

    def _notify(self):
        pass