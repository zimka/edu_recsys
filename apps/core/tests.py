import random
from collections import Counter
from uuid import uuid4

from django.test import TestCase

from apps.context.models import Activity, Student
from apps.core.recommender import ConstRecommender
from .raw_recommendation import RawRecommendation
from .api_utils import RecommendationSerializer


def create_test_user(id=None):
    if id is None:
        id = random.randint(0, 1000)
    Student.objects.create(uid=id, leader_id=random.randint(0, 1000))


def create_test_activity(title=None):
    if title is None:
        title = "Act{}".format(random.randint(0, 1000))
    Activity.objects.create(title=title)


class BaseActRecTestCase(TestCase):
    N_USERS = 3
    N_ACTS = 4

    def setUp(self):
        for n in range(self.N_USERS):
            create_test_user(n)

        for n in range(self.N_ACTS):
            create_test_activity(title="Act{}".format(n))


class RecommendationObjectTest(BaseActRecTestCase):
    def test_recommendation_creation(self):
        r = RawRecommendation.from_kwargs(
            user=Student.objects.first(),
            item=Activity.objects.first(),
            score=0.42,
            source="test"
        )
        self.assertTrue(r.created is None)
        kw = r.to_kwargs()
        all_in = "user" in kw and "item" in kw and "score" in kw
        self.assertTrue(all_in)

    def test_comparison(self):
        r1 = RawRecommendation.from_kwargs(
            user=Student.objects.first(),
            item=Activity.objects.first(),
            score=0.42,
            source="test"
        )

        r2 = RawRecommendation.from_kwargs(
            user=Student.objects.first(),
            item=Activity.objects.first(),
            score=0.42,
            source="test"
        )
        self.assertTrue(r1 == r2)
        r2.score = 0.5
        self.assertFalse(r1 != r2)

    def test_serialization(self):
        r1 = RawRecommendation.from_kwargs(
            user=Student.objects.first(),
            item=Activity.objects.first(),
            score=0.42,
            source="test"
        )
        data = RecommendationSerializer(r1).data
        self.assertTrue(isinstance(data, dict))
        self.assertTrue(set(data.keys()) == {'created', 'score', 'user', 'item'})
        r2 = RawRecommendation.from_kwargs(
            user=Student.objects.first(),
            item=Activity.objects.first(),
            score=0.99,
            source="test"
        )
        data = RecommendationSerializer([r1,r2], many=True).data
        self.assertTrue(len(data) == 2)


class ActivityRecommendersTestCase(BaseActRecTestCase):
    def test_const_for_all(self):
        lvl = 0.25
        cr25 = ConstRecommender(score_const=lvl)

        recs = cr25.get_recommendations()
        rnd = lambda x: int(x * 100)
        self.assertTrue(all([rnd(r.score) == rnd(lvl) for r in recs]))

        users = Counter([r.user.leader_id for r in recs])
        self.assertTrue(len(users) == self.N_USERS)
        self.assertTrue(all([v == self.N_ACTS for k, v in users.items()]))

    def test_const_for_usergroup(self):
        lvl = 0.35
        cr35 = ConstRecommender(score_const=lvl)

        users = Student.objects.all()
        length = int(len(users)/2)
        users = [users[i] for i in range(length)]
        self.assertTrue(len(users) == length)

        recs = cr35.get_recommendations(users)
        rnd = lambda x: int(x * 100)
        self.assertTrue(all([rnd(r.score) == rnd(lvl) for r in recs]))

        users = Counter([str(r.user) for r in recs])
        self.assertTrue(all([v == self.N_ACTS for k, v in users.items()]))

    def test_const_for_activity_filter(self):
        lvl = 0.45
        cr35 = ConstRecommender(score_const=lvl)
        activity_filter = lambda x: x.title != "Act0"

        recs = cr35.get_recommendations(item_filter=activity_filter)
        rnd = lambda x: int(x * 100)
        self.assertTrue(all([rnd(r.score) == rnd(lvl) for r in recs]))

        users = Counter([str(r.user) for r in recs])
        self.assertTrue(len(users) == self.N_USERS)
        self.assertTrue(all([v == (self.N_ACTS - 1) for k, v in users.items()]))