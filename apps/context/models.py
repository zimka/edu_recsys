from abc import ABCMeta, abstractmethod, abstractclassmethod
import uuid

from django.db import models
from model_utils.models import SoftDeletableModel


class LoadableDumb:
    def load(self):
        pass

    @classmethod
    def load_bulk(cls):
        pass


class Activity(SoftDeletableModel, LoadableDumb):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField()
    #TODO: ForeignKey IsleContext

    def __str__(self):
        return self.title


class Student(SoftDeletableModel, LoadableDumb):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    leader_id = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return str(self.leader_id)

    @property
    def is_complete(self):
        return self.digital_profile is not None


class IsleContext(SoftDeletableModel, LoadableDumb):
    name = models.CharField(max_length=255)

    @classmethod
    def get_from_name(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_default(cls):
        # TODO: добавить дефолт
        cnt = cls.objects.first()
        if not cnt:
            raise ValueError("No contexts at all!")

    def __str__(self):
        return self.name