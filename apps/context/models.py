import uuid

from django.db import models
from django.conf import settings
from model_utils.models import SoftDeletableModel

direction_uuids = settings.DIRECTION_UUIDS


class Directions:

    DATA_ANALYST = direction_uuids['DATA_ANALYST']
    BUSINESS_ARCHITECT = direction_uuids['BUSINESS_ARCHITECT']
    ORGANIZER = direction_uuids['ORGANIZER']
    ENTREPRENEUR = direction_uuids['ENTREPRENEUR']
    COMMUNITY_LEADER = direction_uuids['COMMUNITY_LEADER']
    TECHNOLOGIST = direction_uuids['TECHNOLOGIST']

    KEYS = (DATA_ANALYST, BUSINESS_ARCHITECT, ORGANIZER, ENTREPRENEUR, COMMUNITY_LEADER, TECHNOLOGIST)


class LoadableDumb:
    def load(self):
        pass

    @classmethod
    def load_bulk(cls):
        pass


class Activity(SoftDeletableModel, LoadableDumb):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    #TODO: ForeignKey IsleContext

    def __str__(self):
        return self.title

    def get_uid(self):
        return self.uuid


class Student(SoftDeletableModel, LoadableDumb):
    uid = models.IntegerField(editable=False, unique=True)
    leader_id = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return str(self.uid)

    @classmethod
    def get(cls, uid, create=False):
        if not isinstance(uid, int):
            return None
        try:
            if create:
                student, created = cls.objects.get_or_create(uid=uid)
                return student
            else:
                return cls.objects.get(uid=uid)
        except cls.DoesNotExist:
            return None

    def get_uid(self):
        return self.uid

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