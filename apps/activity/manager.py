from apps.context.models import Student
from apps.core.manager import AbstractRecommendationManager
from apps.core.recommender import ConstRecommender
from .models import ActivityRecommendationFresh, ActivityRecommendationLogs


class ActivityRecommendationManager(AbstractRecommendationManager):
    """
    Менеджер рекомендаций активностей. Вызывает расчеты, сохраняет результаты,
    выдает по запросу
    """
    def __init__(self, forced_config=None):
        super().__init__()
        self.forced_config = forced_config

    def do_update(self, item_filter=lambda x: True):
        config = self.forced_config or self.get_groups_config()

        pipeline = list(getattr(self, name) for name in ["_filter_recommendations", "_to_logs", "_to_fresh"])
        for recommender, users in config.items():
            recommendations = recommender.get_recommendations(users=users, item_filter=item_filter)
            for meth in pipeline:
                recommendations = meth(recommendations)

    def do_single_update(self, user, item_filter=lambda x: True):
        config = self.forced_config or self.get_groups_config()

        pipeline = list(getattr(self, name) for name in ["_filter_recommendations", "_to_logs", "_to_fresh"])
        for recommender, users in config.items():
            if user not in users:
                continue
            recommendations = recommender.get_recommendations(users=[user], item_filter=item_filter)
            for meth in pipeline:
                recommendations = meth(recommendations)

    def get_groups_config(self):
        return {
            ConstRecommender(): Student.objects.all()
        }

    def get_recommendations(self, created_after=None, user_uuid=None):
        # TODO: добавить логирование выдачи на уровне этого метода?

        qs = ActivityRecommendationFresh.get_fresh_queryset(created_after=created_after)
        qs = qs.prefetch_related('user').prefetch_related('item')
        if user_uuid:
            qs = qs.filter(user__uuid=user_uuid)
        return qs

    def _filter_recommendations(self, recommendations):
        # TODO: top score filtering
        return recommendations

    def _to_fresh(self, recommendations):
        ActivityRecommendationFresh.put_items(recommendations)
        return recommendations

    def _to_logs(self, recommendations):
        # TODO: add logging
        ActivityRecommendationLogs.put_items(recommendations)
        return recommendations
