from apps.activity.manager import ActivityRecommendationManager
from celery import shared_task
import logging
log = logging.getLogger(__name__)


def update_single_user_recommendations(user):
    ActivityRecommendationManager().do_single_update(user)


def build_profile(user_diagnostics, load_user_data=True, update_recommendations=True):
    from apps.digital_profile.models import DigitalProfile

    student = user_diagnostics.user
    if load_user_data:
        student.load()
    dp, created = DigitalProfile.objects.get_or_create(user=user_diagnostics.user)
    data = user_diagnostics.data
    try:
        _update_data(dp, data)
    except Exception as e:
        log.error("Error processing users '{}' profile:{}".format(dp.user.uuid, str(e)))
        return False
    if update_recommendations:
        update_single_user_recommendations(student)
    return True

def _update_data(dp, data):
    data['some_key'] = "some_changes"
    dp.archetypes = data
    dp.save()


@shared_task
def build_profile_async(user_diagnostics):
    build_profile(user_diagnostics)