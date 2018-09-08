import logging
from uuid import uuid4
from django.db import models
from jsonfield import JSONField
from apps.context.models import Student, Directions
from .tasks import compute_single_score_async
from .clients import DpApiClient, LrsApiClient, PleApiClient


log = logging.getLogger(__name__)


class ComputeTask(models.Model):
    # TODO: change db to postgres and use native json. JSONFields
    input = JSONField(default={})
    output = JSONField(default={})
    complete = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def compute(self):
        pass


class SingleScoreComputeTask(ComputeTask):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(Student, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.user)

    def compute_async(self):
        compute_single_score_async.delay(self.uuid)

    def compute(self):
        if not self.input:
            self._fetch_input()
        if not self.output:
            self._compute_score()
        if not self.complete:
            self._notify()
        self.save()

    def _fetch_input(self):
        input = {}
        diagnostics = PleApiClient().get_user_diagnostics(self.user.uid)
        if diagnostics is not None:
            input.update(diagnostics)
        archetypes = LrsApiClient().get_archetypes(self.user.uid)
        if archetypes is not None:
            input.update(archetypes)
        self.input = input

    def _compute_score(self):
        def hack():
            import random
            result = {}
            for k in Directions.KEYS:
                result[k] = random.randint(0, 100)
            return result
        h = hack()
        self.output = h

    def _notify(self):
        success = DpApiClient().set_single_score(self.user.uid, self.output)
        if success:
            self.complete = True
