import logging
from celery import shared_task
from apps.context.models import Student
from .models import NetworkingRecommendation
from .compute import compute_similarities, NetworkingRecommender

log = logging.getLogger(__name__)


@shared_task
def create_networking_recommendations(for_new_only=False):
   _update_all_recommendations(for_new_only)


def _update_all_recommendations(for_new_only, save=True, single_student_uid=None, starting_contact_uids=[]):
    log.info("Started recommendation update : for_new_only={}, save={}, student={}".format(
        for_new_only, save, single_student_uid
    ))
    students = Student.objects.all()
    validated_students, sim_competence, sim_experience, sim_interest = compute_similarities(students)
    recommender = NetworkingRecommender(
        experience_similarity=sim_experience,
        competence_similarity=sim_competence,
        interest_similarity=sim_interest,
        teammates_by_id={}
    )
    if for_new_only:
        has_recs = set(n.user for n in NetworkingRecommendation.objects.all())
        all_users = set(validated_students)
        validated_students = list(all_users - has_recs)
    results = []
    for vst in validated_students:
        if single_student_uid is not None and vst.uid!=single_student_uid:
            continue
        recs = {}
        current_list = starting_contact_uids.copy()
        recs['coffee'] = recommender.recommend_man(vst.uid, current_list, 'experience')[0]
        current_list.append(recs['coffee'])
        recs['look'] = recommender.recommend_man(vst.uid, current_list, 'competences')[0]
        current_list.append(recs['look'])
        recs['discuss'] = recommender.recommend_man(vst.uid, current_list, 'interests')[0]
        current, created = NetworkingRecommendation.objects.get_or_create(user=vst)
        current.recommendations = {"communication": [
            {"type": 'coffee', 'target_ids':[recs['coffee']]},
            {"type": 'discuss', 'target_ids': [recs['discuss']]},
            {"type": 'look', 'target_ids': [recs['look']]}
        ]}
        results.append(current)
        if save:
            current.save()
    return results