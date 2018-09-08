import logging
from uuid import uuid4, UUID
from django.db import models
from jsonfield import JSONField
from model_utils.fields import AutoCreatedField
from apps.context.models import Student
from .tasks import compute_single_score_async
from .clients import DpApiClient, LrsApiClient, PleApiClient


log = logging.getLogger(__name__)


class ComputeTask(models.Model):
    # TODO: change db to postgres and use native json. JSONFields
    input = JSONField(default={})
    output = JSONField(default={})
    complete = models.BooleanField(default=False)
    created = AutoCreatedField()
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
        from .compute.v0 import compute_v0
        self.output = compute_v0(self.input)

    def _notify(self):
        success = DpApiClient().set_single_score(self.user.uid, self.output)
        if success:
            self.complete = True


class PleQuestionIdUuidMap(models.Model):
    """
    100% костыль
    """
    uuid = models.UUIDField()
    ple_id = models.IntegerField()

    @classmethod
    def get_id_by_uuid(cls, question_uuid):
        if isinstance(question_uuid, str):
            question_uuid = UUID(question_uuid)
        try:
            return cls.objects.get(uuid=question_uuid).ple_id
        except cls.DoesNotExist:
            return None
