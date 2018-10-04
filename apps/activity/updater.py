from edu_common.models import Student
from recsys_base.recommender import ConstRecommender
from recsys_base.updater import RecommendationUpdater
from .models import ActivityRecommendation, Activity


class ActivityRecommendationUpdater(RecommendationUpdater):
    """
    Обновляет рекомендации активностей
    """
    def __init__(self, recommender_users_config=None):
        super().__init__(recommender_users_config or {
            ConstRecommender(items_space=Activity.objects.all()): Student.objects.all()
        })

    def do_update(self, item_filter=lambda x: True):
        return self._do_update(item_filter=item_filter)

    def do_single_update(self, user, item_filter=lambda x: True):
        single_user_filter = lambda x: x == user
        return self._do_update(single_user_filter, item_filter)

    def _do_update(self, users_filter=lambda x: True, item_filter=lambda x: True):
        config = self.config
        for recommender, users in config.items():
            users = list(filter(users_filter, users))
            recommendations = recommender.get_recommendations(users=users, item_filter=item_filter)
            ActivityRecommendation.put_many(recommendations)
