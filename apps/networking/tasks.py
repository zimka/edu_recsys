import logging
from celery import shared_task
from apps.context.models import Student
from .models import NetworkingRecommendation
from .recommender import TripleNetworkingRecommender

log = logging.getLogger(__name__)


@shared_task
def create_networking_recommendations(for_new_only=False):
    update_network_recommendations(for_new_only)


def update_network_recommendations(for_new_only=False, single_user_uid=None):
    log.info("Started recommendation update : for_new_only={}".format(
        for_new_only
    ))
    students = Student.objects.all()
    recommender = TripleNetworkingRecommender(items_space=students)
    if single_user_uid:
        users_for = all(filter(lambda x:x.uid==single_user_uid, students))
    else:
        users_for = students
    if for_new_only:
        has_recs = set(n.user for n in NetworkingRecommendation.objects.all())
        all_users = set(students)
        users_for = list(all_users - has_recs)

    cmp_recs, int_recs, exp_recs = recommender.get_recommendations(users=users_for)
    NetworkingRecommendation.put_items(cmp_recs, options={"type": "cmp"})
    NetworkingRecommendation.put_items(int_recs, options={"type": "int"})
    NetworkingRecommendation.put_items(int_recs, options={"type": "exp"})
