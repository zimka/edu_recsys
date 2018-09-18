import random
from abc import ABC, abstractmethod

from .raw_recommendation import RawRecommendation, in_score_limits


def get_all_users():
    from apps.context.models import Student
    return Student.objects.all()



class AbstractRecommender(ABC):
    """
    Именованный рекомендатор. Для заданных юзеров рассчитывает рекомендации
    по объектам, удовлетворяющим фильтру
    """

    @abstractmethod
    def get_recommendations(self, users=tuple(), item_filter=lambda x: True):
        pass

    @abstractmethod
    def _get_recommendations(self, users, items):
        pass

    @abstractmethod
    def get_name(self):
        pass


class BaseRecommender(AbstractRecommender):
    def __init__(self, *, items_space, **kwargs):
        self.items_space = items_space

    def get_recommendations(self, users=tuple(), item_filter=lambda x: True):
        if not users:
            users = get_all_users()
        items = list(filter(item_filter, self.items_space))
        return self._get_recommendations(users, items)


class DumbRecommender(BaseRecommender):
    def get_name(self):
        return "dumb"

    def _get_recommendations(self, users, items):
        recs = []
        name = self.get_name()
        for u in users:
            for a in items:
                recs.append(RawRecommendation.from_kwargs(
                    user=u,
                    item=a,
                    score=self._get_score(),
                    source=name,
                ))
        return recs

    def _get_score(self):
        pass


class RandomRecommender(DumbRecommender):
    def _get_score(self):
        return random.random()


class ConstRecommender(DumbRecommender):
    def __init__(self, *, items_space, **kwargs):
        super().__init__(items_space=items_space, **kwargs)
        score_const = kwargs.get('score_const', 0.42)

        if not in_score_limits(score_const):
            raise ValueError("score_const {} not in score limits".format(score_const))
        self.score_const = score_const

    def _get_score(self):
        return self.score_const
