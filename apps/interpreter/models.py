import logging
from uuid import uuid4, UUID

from django.db import models
from jsonfield import JSONField
from model_utils.fields import AutoCreatedField

from edu_coresys.models import Student
from edu_coresys.clients import DpApiClient, LrsApiClient, PleApiClient
from .tasks import run_update

log = logging.getLogger(__name__)


class ComputeTask(models.Model):
    """
    Задача на расчет чего-либо
    """
    input = JSONField(default={})
    output = JSONField(default={})
    complete = models.BooleanField(default=False)
    created = AutoCreatedField()

    class Meta:
        abstract = True

    def compute(self):
        pass


class SingleScoreComputeTask(ComputeTask):
    """
    Задача на расчет интерпретатором v0 цифрового профиля
    юзера. Input собирается из систем контура
    """
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(Student, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.user)

    @classmethod
    def run_for_user(cls, user):
        task = cls.objects.create(user=user)
        task.compute_async()

    def compute_async(self):
        run_update(self.uuid)

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
        client = LrsApiClient()
        archetypes = client.get_archetypes(self.user.uid)
        motivalis = client.get_motivalis(self.user.uid)
        if archetypes is not None:
            input.update({client.archetypes_guid + "_archetypes": archetypes})
        if archetypes is not None:
            input.update({client.archetypes_guid + "_motivalis": motivalis})
        self.input = input

    def _compute_score(self, add_motibalis_archetypes=True):
        from .compute.v0 import compute_v0, add_archetype_motivalis_uuids
        self.output = compute_v0(self.input)
        if add_motibalis_archetypes:
            self.output.update(add_archetype_motivalis_uuids(self.input))

    def _notify(self):
        success = DpApiClient().set_single_score(self.user.uid, self.output)
        if success:
            self.complete = True


class PleQuestionIdUuidMap(models.Model):
    """
    100% костыль, необходимый для перевода uuid-ов вопросов
    в PLE в id, отражаемый пользователям
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
