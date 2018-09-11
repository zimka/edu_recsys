import logging
from celery import shared_task
from apps.context.models import Student
from .models import NetworkingRecommendation
from .compute import compute_similarities, NetworkingRecommender

log = logging.getLogger(__name__)


@shared_task
def create_networking_recommendations(overwrite):
   _update_all_recommendations(overwrite)


def _update_all_recommendations(overwrite):
    students = Student.objects.all()
    validated_students, sim_competence, sim_experience, sim_interest = compute_similarities(students)
    recommender = NetworkingRecommender(
        experience_similarity=sim_experience,
        competence_similarity=sim_competence,
        interest_similarity=sim_interest,
        teammates_by_id={}
    )
    if not overwrite:
        has_recs = set(n.user for n in NetworkingRecommendation.objects.all())
        all_users = set(validated_students)
        validated_students = list(all_users - has_recs)

    for vst in validated_students:
        recs = {}
        recs['coffee'] = recommender.recommend_man(vst.uid, [], 'experience')[0]
        recs['look'] = recommender.recommend_man(vst.uid, [recs['coffee']], 'competences')[0]
        recs['discuss'] = recommender.recommend_man(vst.uid, [recs['coffee'], recs['look']], 'interests')[0]
        current, created = NetworkingRecommendation.objects.get_or_create(user=vst)
        current.recommendations = {"communication": [
            {"type": 'coffee', 'target_ids':[recs['coffee']]},
            {"type": 'discuss', 'target_ids': [recs['discuss']]},
            {"type": 'look', 'target_ids': [recs['look']]}
        ]}
        current.save()
