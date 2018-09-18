from abc import abstractmethod, ABCMeta
from .tasks import update_recommendations
from django.core.serializers import serialize


class AbstractRecommendationManager(metaclass=ABCMeta):
    """
    Интерфейс к рекомендациям. Позволяет получать, обновлять рекомендации (синхронно/асинхронно)
    и распределять пользователей по разным методам рекомендации
    """
    def run_update_async(self, **kwargs):
        update_recommendations.delay(self, **kwargs)

    @abstractmethod
    def do_update(self, **kwargs):
        pass

    @abstractmethod
    def get_groups_config(self):
        pass

    @abstractmethod
    def get_recommendations(self, created_after=None, user_uuid=None):
        pass
