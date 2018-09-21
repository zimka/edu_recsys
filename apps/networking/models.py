from django.db import models
from apps.context.models import Student
from apps.core.models import AbstractRecommendation, MutableMixin


class NetworkingRecommendation(MutableMixin, AbstractRecommendation):

    class Meta:
        abstract = True


class CompetenceNetworkingRecommendation(NetworkingRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_cmp")


class InterestNetworkingRecommendation(NetworkingRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_int")


class ExperienceNetworkingRecommendation(NetworkingRecommendation):
    CLEAR_UPDATE_USERS = True
    item = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="recommended_user_exp")
