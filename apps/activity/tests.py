from django.db.utils import IntegrityError

from apps.context.models import Student, Activity
from apps.core.recommender import ConstRecommender
from apps.core.raw_recommendation import RawRecommendation
from apps.core.api_utils import RecommendationSerializer
from apps.core.tests import BaseActRecTestCase

from .manager import ActivityRecommendationManager
from .models import ActivityRecommendationFresh, ActivityRecommendationLogs


def get_test_config(lvl=0.42):
    return {
        ConstRecommender(score_const=lvl): Student.objects.all()
    }


class ActivityRecommenderManagerTestCase(BaseActRecTestCase):
    def test_manager_update(self):
        lvl = 0.45
        man = ActivityRecommendationManager(forced_config=get_test_config(lvl))
        man.do_update()
        recs = ActivityRecommendationFresh.objects.all()
        self.assertTrue(len(recs) == self.N_USERS * self.N_ACTS)

        recs = ActivityRecommendationLogs.objects.all()
        self.assertTrue(len(recs) == self.N_USERS * self.N_ACTS)


class ActivityRecommendationTestCase(BaseActRecTestCase):
    def setUp(self):
        super().setUp()
        self.lvl = 0.3
        self.lvl2 = 0.5

        man = ActivityRecommendationManager(forced_config=get_test_config(self.lvl))
        man.do_update()

        man = ActivityRecommendationManager(forced_config=get_test_config(self.lvl2))
        man.do_update()

    def test_creation_from_recommendation(self):
        u = Student.objects.first()
        a = Activity.objects.first()

        raw = RawRecommendation.from_kwargs(user=u, item=a, score=0.42, source="test")
        res = ActivityRecommendationLogs.create_from_raw(raw)

        self.assertTrue(res.user == raw.user)
        self.assertTrue(res.item == raw.item)
        self.assertTrue(res.score == raw.score)
        self.assertTrue(res.created is not None)

    def test_constrains_vilolation_user(self):
        a = Activity.objects.first()
        raw = RawRecommendation.from_kwargs(user=None, item=a, score=0.42, source="test")
        with self.assertRaises(IntegrityError) as cm:
            ActivityRecommendationLogs.create_from_raw(raw)

    def test_constrains_violation_item(self):
        u = Student.objects.first()
        raw = RawRecommendation.from_kwargs(user=u, item=None, score=0.42, source="test")
        with self.assertRaises(IntegrityError) as cm:
            ActivityRecommendationLogs.create_from_raw(raw)

    def test_get_fresh_all(self):
        recs = ActivityRecommendationFresh.objects.all()
        self.assertTrue(len(recs) == self.N_USERS * self.N_ACTS)
        self.assertTrue(all([x.score == self.lvl2 for x in recs]))

        users = set([r.user for r in recs])
        self.assertTrue(len(users) == self.N_USERS)

        items = set([r.item for r in recs])
        self.assertTrue(len(items) == self.N_ACTS)

    def test_get_logs_all(self):
        recs = ActivityRecommendationLogs.objects.all()
        self.assertTrue(len(recs) == 2 * self.N_USERS * self.N_ACTS)

    def test_serialization(self):
        single = ActivityRecommendationFresh.objects.first()
        serial = RecommendationSerializer(single)
        many = ActivityRecommendationFresh.objects.all()
        serial = RecommendationSerializer(many, many=True)
        self.assertTrue(len(serial.data) == len(many))
