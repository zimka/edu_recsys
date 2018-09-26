from edu_coresys.models import Student
from apps.core.recommender import BaseRecommender, RawRecommendation
from .compute import SimilarityBasedNetworkingRecommender
from .compute.compute_prereq import compute_similarities


class TripleNetworkingRecommender(BaseRecommender):
    """
    Рекоммендатор, рассчитывающий сразу три рекомендации: по опыту, интересам и компетенциям
    """
    def get_name(self):
        return "triple"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.items_space is None:
            self.items_space = Student.objects.all()

    def _get_recommendations(self, users, items):
        if not all([x in items for x in users]):
            # Иначе не будет рассчитана similarity
            raise ValueError("All users who get recommendations must be in item list")

        name = self.get_name()

        staff_uids = [x.uid for x in Student.objects.filter(is_staff=True)]

        sim_competence, sim_experience, sim_interest = compute_similarities(items)
        print(sim_experience.shape)
        backend_recommender = SimilarityBasedNetworkingRecommender(
            experience_similarity=sim_experience,
            competence_similarity=sim_competence,
            interest_similarity=sim_interest,
            teammates_by_id={}
        )
        int_recs = []
        exp_recs = []
        cmp_recs = []
        for vst in users:
            current_list = staff_uids.copy()
            int_id, int_score = backend_recommender.recommend_man(vst.uid, current_list, 'interests')
            current_list.append(int_id)
            exp_id, exp_score = backend_recommender.recommend_man(vst.uid, current_list, 'experience')
            current_list.append(exp_id)
            cmp_id, cmp_score = backend_recommender.recommend_man(vst.uid, current_list, 'competences')
            print(int_id, exp_id, cmp_id)
            int_user = next(filter(lambda x: x.uid == int_id, items))
            exp_user = next(filter(lambda x: x.uid == exp_id, items))
            cmp_user = next(filter(lambda x: x.uid == cmp_id, items))
            if int_user:
                int_recs.append(RawRecommendation.from_kwargs(user=vst, item=int_user, score=int_score, source=name))
            if exp_user:
                exp_recs.append(RawRecommendation.from_kwargs(user=vst, item=exp_user, score=exp_score, source=name))
            if cmp_user:
                cmp_recs.append(RawRecommendation.from_kwargs(user=vst, item=cmp_user, score=cmp_score, source=name))
        return cmp_recs, exp_recs, int_recs
