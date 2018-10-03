from abc import ABC, abstractmethod


class RecommendationUpdater(ABC):
    """
    Интерфейс для расчета и обновления рекоммендаций.
    Получает конфиг рекоммендаторов в формате Dict[Recommender, List[User]]
    и применяет рекоммендатор для соответствующих юзеров
    """
    def __init__(self, recommender_users_config=None, **kwargs):
        self.config = recommender_users_config

    @abstractmethod
    def do_update(self, item_filter=lambda x: True):
        raise NotImplemented

    @abstractmethod
    def do_single_update(self, user, item_filter=lambda x: True):
        raise NotImplemented
