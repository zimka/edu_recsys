"""
Рекоммендации пользователю по нетворкингу.
На данный момент даются одновременно рекоммендации
по трем направлениям: интересам, опыту и компетенциям.
"""
from django.db import models

from edu_common.models import Student
from edu_common.clients import PleApiClient
from recsys_base.models import AbstractRecommendation

from jsonfield import JSONField
from model_utils.fields import AutoLastModifiedField

class CompetenceNetworkingRecommendation(AbstractRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_cmp")


class InterestNetworkingRecommendation(AbstractRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_int")


class ExperienceNetworkingRecommendation(AbstractRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_exp")


class NetworkingInfoStorage(models.Model):
    user = models.ForeignKey(Student, on_delete=models.PROTECT)
    info = JSONField(default={})
    updated = AutoLastModifiedField()

    def fetch_info(self):
        self.info = PleApiClient().get_user_diagnostics(self.user.uid)
        self.save()

    @classmethod
    def update_for_users(cls, users):
        nis = cls.objects.get(user__in=users)
        new_users = list(set(users) - set(x.user for x in nis))
        new_nis = [cls.objects.create(user=u) for u in new_users]
        for x in nis:
            x.fetch_info()
            x.save()
        for x in new_nis:
            x.fetch_info()
            x.save()
