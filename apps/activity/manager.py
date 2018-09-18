from apps.context.models import Student
from apps.core.manager import AbstractRecommendationManager
from apps.core.recommender import ConstRecommender
from .models import ActivityRecommendationFresh, ActivityRecommendationLogs, Activity
from datetime import datetime
import pytz


class ActivityRecommendationManager(AbstractRecommendationManager):
    """
    Менеджер рекомендаций активностей. Вызывает расчеты, сохраняет результаты,
    выдает по запросу
    """
    def __init__(self, forced_config=None):
        super().__init__()
        self.forced_config = forced_config

    def do_update(self, item_filter=lambda x: True):
        return self._do_update(item_filter=item_filter)

    def do_single_update(self, user, item_filter=lambda x: True):
        single_user_filter = lambda x: x == user
        return self._do_update(single_user_filter, item_filter)

    def _do_update(self, users_filter=lambda x: True, item_filter=lambda x: True):
        config = self.forced_config or self.get_groups_config()
        pipeline = list(getattr(self, name) for name in ["_modify", "_log", "_save"])
        for recommender, users in config.items():
            users = filter(users_filter, users)
            recommendations = recommender.get_recommendations(users=users, item_filter=item_filter)
            for meth in pipeline:
                recommendations = meth(recommendations)

    def get_groups_config(self):
        return {
            ConstRecommender(items_space=Activity.objects.all()): Student.objects.all()
        }

    def get_recommendations(self, created_after=None, user_uid=None):
        # TODO: добавить логирование выдачи на уровне этого метода?

        qs = ActivityRecommendationFresh.get_fresh_queryset(created_after=created_after)
        qs = qs.prefetch_related('user').prefetch_related('item')
        if user_uid:
            qs = qs.filter(user__uid=user_uid)
        return qs

    def _modify(self, recommendations):
        now = datetime.now(pytz.utc)
        for r in recommendations:
            r.created = now
        return recommendations

    def _save(self, recommendations):
        ActivityRecommendationFresh.put_items(recommendations)
        return recommendations

    def _log(self, recommendations):
        # TODO: add logging
        ActivityRecommendationLogs.put_items(recommendations)
        return recommendations
