import uuid

from django.db import models
from model_utils.models import SoftDeletableModel


class Activity(SoftDeletableModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField()

    def __str__(self):
        return self.title


class Student(SoftDeletableModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    leader_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.leader_id)
