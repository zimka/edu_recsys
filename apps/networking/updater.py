from edu_common.models import Student
from recsys_base.updater import RecommendationUpdater
from .models import InterestNetworkingRecommendation, \
    ExperienceNetworkingRecommendation, CompetenceNetworkingRecommendation
from .recommender import TripleNetworkingRecommender


class NetworkingRecommendationUpdater(RecommendationUpdater):
    """
    Обновляет рекомендации нетворкинга
    """
    def __init__(self, recommender_users_config=None, for_new_only=False):
        super().__init__( recommender_users_config or {
            TripleNetworkingRecommender(items_space=Student.objects.all()): Student.objects.all()
        })
        self.for_new_only = for_new_only

    def do_update(self, item_filter=lambda x: True):
        return self._do_update(item_filter=item_filter)

    def do_single_update(self, user, item_filter=lambda x: True):
        single_user_filter = lambda x: x == user
        return self._do_update(single_user_filter, item_filter)

    def _do_update(self, users_filter=lambda x: True, item_filter=lambda x: True):
        config = self.config
        if self.for_new_only:
            users_with_recs = set(x.uid for x in CompetenceNetworkingRecommendation.objects.all())
            updated_users_filter = lambda x: users_filter(x) and x.uid not in users_with_recs
        else:
            updated_users_filter = users_filter

        for recommender, users in config.items():
            users = list(filter(updated_users_filter, users))
            cmp_recs, exp_recs, int_recs = recommender.get_recommendations(users=users, item_filter=item_filter)
            print(len(cmp_recs))
            CompetenceNetworkingRecommendation.put_many(cmp_recs)
            ExperienceNetworkingRecommendation.put_many(exp_recs)
            InterestNetworkingRecommendation.put_many(int_recs)
