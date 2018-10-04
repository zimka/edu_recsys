import random

from django.db.utils import IntegrityError

from edu_common.models import Student, Activity
from recsys_base.raw_recommendation import RawRecommendation
from recsys_base.recommender import ConstRecommender
from recsys_base.tests import TestCase, create_test_user
from .api_utils import ActivityRecommendationSerializer
from .models import ActivityRecommendation
from .updater import ActivityRecommendationUpdater


def get_test_config(lvl=0.42, items_space=None):
    if items_space is None:
        items_space = Activity.objects.all()
    return {
        ConstRecommender(items_space=items_space, score_const=lvl): Student.objects.all()
    }


def create_test_activity(title=None):
    if title is None:
        title = "Act{}".format(random.randint(0, 1000))
    Activity.objects.create(title=title)


class ActivityTestCase(TestCase):
    N_USERS = 3
    N_ACTS = 4

    def setUp(self):
        for n in range(self.N_USERS):
            create_test_user(n)

        for n in range(self.N_ACTS):
            create_test_activity(title="Act{}".format(n))

class ActivityRecommenderManagerTestCase(ActivityTestCase):
    def test_manager_update(self):
        lvl = 0.45
        man = ActivityRecommendationUpdater(recommender_users_config=get_test_config(lvl))
        man.do_update()
        recs = ActivityRecommendation.objects.all()
        self.assertTrue(len(recs) == self.N_USERS * self.N_ACTS)

        recs = ActivityRecommendation.history.all()
        self.assertTrue(len(recs) == self.N_USERS * self.N_ACTS)

    def test_manager_single_update(self):
        lvl = 0.5
        man = ActivityRecommendationUpdater(recommender_users_config=get_test_config(lvl))
        u = Student.objects.first()
        self.assertFalse(len(ActivityRecommendation.history.all()))
        man.do_single_update(u)
        self.assertTrue(len(ActivityRecommendation.history.all()) == self.N_ACTS)
        generated_users = set(x.user for x in ActivityRecommendation.history.all())
        self.assertTrue(len(generated_users) == 1)
        self.assertTrue(list(generated_users)[0] == u)

    def test_update_changes_fresh_created(self):
        lvl = 0.3
        man = ActivityRecommendationUpdater(recommender_users_config=get_test_config(lvl))

        man.do_update()
        recs = ActivityRecommendation.objects.all()
        highest_date = max([x.created for x in recs])
        man.do_update()
        recs = ActivityRecommendation.objects.all()
        self.assertTrue(all([x.created > highest_date for x in recs]))


class ActivityRecommendationTestCase(ActivityTestCase):
    def setUp(self):
        super().setUp()
        self.lvl = 0.3
        self.lvl2 = 0.5

        man = ActivityRecommendationUpdater(recommender_users_config=get_test_config(self.lvl))
        man.do_update()

        man = ActivityRecommendationUpdater(recommender_users_config=get_test_config(self.lvl2))
        man.do_update()

    def test_single_override(self):
        res = ActivityRecommendation.objects.first()
        new_score = 0.99
        res.score = new_score
        res.save()
        res = ActivityRecommendation.objects.get(user=res.user, item=res.item)
        self.assertTrue(res.score == new_score)

    def test_creation_from_recommendation(self):
        u = Student.objects.first()
        a = Activity.objects.first()

        raw = RawRecommendation.from_kwargs(user=u, item=a, score=0.42, source="test")
        ActivityRecommendation.put_single(raw)

        res = ActivityRecommendation.objects.get(user=u, item=a)

        self.assertTrue(res.user == raw.user)
        self.assertTrue(res.item == raw.item)
        self.assertTrue(res.score == raw.score)
        self.assertTrue(res.created is not None)

    def test_override_from_put_items(self):
        u = Student.objects.first()
        a = Activity.objects.first()

        raw = RawRecommendation.from_kwargs(user=u, item=a, score=0.42, source="test")
        ActivityRecommendation.put_many([raw])
        res = ActivityRecommendation.objects.get(user=u, item=a)

        self.assertTrue(res.user == raw.user)
        self.assertTrue(res.item == raw.item)
        self.assertTrue(res.score == raw.score)
        self.assertTrue(res.created is not None)

    def test_constrains_vilolation_user(self):
        a = Activity.objects.first()
        raw = RawRecommendation.from_kwargs(user=None, item=a, score=0.42, source="test")
        with self.assertRaises(IntegrityError) as cm:
            ActivityRecommendation.put_single(raw)

    def test_constrains_violation_item(self):
        u = Student.objects.first()
        raw = RawRecommendation.from_kwargs(user=u, item=None, score=0.42, source="test")
        with self.assertRaises(IntegrityError) as cm:
            ActivityRecommendation.put_single(raw)

    def test_get_fresh_all(self):
        recs = ActivityRecommendation.objects.all()
        self.assertTrue(len(recs) == self.N_USERS * self.N_ACTS)
        self.assertTrue(all([x.score == self.lvl2 for x in recs]))

        users = set([r.user for r in recs])
        self.assertTrue(len(users) == self.N_USERS)

        items = set([r.item for r in recs])
        self.assertTrue(len(items) == self.N_ACTS)

    def test_get_logs_all(self):
        recs = ActivityRecommendation.history.all()
        self.assertTrue(len(recs) == 2 * self.N_USERS * self.N_ACTS)

    def test_serialization(self):
        single = ActivityRecommendation.objects.first()
        serial = ActivityRecommendationSerializer(single)
        many = ActivityRecommendation.objects.all()
        serial = ActivityRecommendationSerializer(many, many=True)
        self.assertTrue(len(serial.data) == len(many))

