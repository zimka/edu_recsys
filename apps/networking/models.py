"""
Рекоммендации пользователю по нетворкингу.
На данный момент даются одновременно рекоммендации
по трем направлениям: интересам, опыту и компетенциям.
"""
from django.db import models

from edu_coresys.models import Student
from apps.core.models import AbstractRecommendation


class CompetenceNetworkingRecommendation(AbstractRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_cmp")


class InterestNetworkingRecommendation(AbstractRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_int")


class ExperienceNetworkingRecommendation(AbstractRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_exp")
