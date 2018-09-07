import uuid

from django.db import models
from model_utils.models import SoftDeletableModel


class Directions:

    DATA_ANALYST = "62ad153e-1974-4249-824b-e60e33bf77f5"
    BUSINESS_ARCHITECT = "24a0e35a-d028-4b7c-a7e6-0672a935bb37"
    ORGANIZER = "c7048753-0f7e-41eb-8923-ae42bbecf6e7"
    ENTREPRENEUR = "9d487640-e482-4d10-ae37-5d11f5fcc9df"
    COMMUNITY_LEADER = "595aa802-0e83-4087-8926-68c1a61d1269"
    TECHNOLOGIST = "dfe15fa8-1bf9-4a71-8790-b05808eaffcc"

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