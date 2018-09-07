from uuid import uuid4
from django.db import models
from jsonfield import JSONField
from apps.context.models import Student, Directions
from .tasks import compute_single_score_async
from .clients import DpApiClient


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
        compute_single_score_async.delay(self.uuid)

    def compute(self):
        import random
        result = {}
        for k in Directions.KEYS:
            result[k] = random.randint(0, 100)
        self.output = result
        self._notify()
        self.complete = True
        self.save()

    def _fetch_input(self):
        pass

    def _notify(self):
        DpApiClient().set_single_score(self.user.uid, self.output)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.complete:
            self.compute_async()
