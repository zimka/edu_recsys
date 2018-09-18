from apps.core.recommender import BaseRecommender, RawRecommendation
from apps.context.models import Student
from .compute.compute_prereq import compute_similarities
from .compute import SimilarityBasedNetworkingRecommender


class TripleNetworkingRecommender(BaseRecommender):

    def get_name(self):
        return "triple_old"

    def get_recommendations(self, users=tuple(), item_filter=lambda x: True):
        if self.items_space is None:
            self.items_space = Student.objects.all()
        all_students = Student.objects.all()
        if not users:
            users = all_students
        target_users = filter(item_filter, all_students)
        if not all([x in target_users for x in users]):
            # Иначе не будет рассчитана similarity
            raise ValueError("All users who get recommendations must be in item list")
        return self._get_recommendations(users, target_users)

    def _get_recommendations(self, users, items):
        name = self.get_name()

        staff_uids = [x.uid for x in Student.objects.filter(staff=True)]

        validated_students, sim_competence, sim_experience, sim_interest = compute_similarities(items)
        backend_recommender = SimilarityBasedNetworkingRecommender(
            experience_similarity=sim_experience,
            competence_similarity=sim_competence,
            interest_similarity=sim_interest,
            teammates_by_id={}
        )
        int_recs = []
        exp_recs = []
        cmp_recs = []

        for vst in validated_students:
            current_list = staff_uids.copy()
            int_id, int_score = backend_recommender.recommend_man(vst.uid, current_list, 'interests')
            current_list.append(int_id)
            exp_id, exp_score = backend_recommender.recommend_man(vst.uid, current_list, 'experience')
            current_list.append(exp_id)
            cmp_id, cmp_score = backend_recommender.recommend_man(vst.uid, current_list, 'competences')

            int_user = next(filter(lambda x: x.uid==int_id, users))
            exp_user = next(filter(lambda x: x.uid==exp_id, users))
            cmp_user = next(filter(lambda x: x.uid==cmp_id, users))
            if int_user:
                int_recs.append(RawRecommendation.from_kwargs(user=vst, item=int_user, score=int_score, source=name))
            if exp_user:
                exp_recs.append(RawRecommendation.from_kwargs(user=vst, item=exp_user, score=exp_score, source=name))
            if cmp_user:
                cmp_recs.append(RawRecommendation.from_kwargs(user=vst, item=cmp_user, score=cmp_score, source=name))
        return cmp_recs, exp_recs, int_recs
