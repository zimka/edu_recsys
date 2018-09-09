import logging
from celery import shared_task
from apps.context.models import Student
from .models import NetworkingRecommendation

log = logging.getLogger(__name__)


@shared_task
def create_networking_recommendations(user_uid):
    try:
        user = Student.objects.get(uid=user_uid)
    except Student.DoesNotExist:
        log.error("Tried to generate networking recommendations for non-existent user {}".format(user_uid))
        return False
    try:
        return NetworkingRecommendation.objects.get(user=user)
    except NetworkingRecommendation.DoesNotExist:
        return NetworkingRecommendation.create(user)

