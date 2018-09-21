from django.test import TestCase
from apps.core.tests import create_test_user
from apps.context.models import Student
from apps.networking.recommender import TripleNetworkingRecommender


class RecommenderTest(TestCase):
    N_USERS = 10

    def setUp(self):
        for n in range(self.N_USERS):
            create_test_user(n)

    def test_all_creation(self):
        users = Student.objects.all()
        recom = TripleNetworkingRecommender(items_space=users)
        cmp_recs, exp_recs, int_recs = recom.get_recommendations()
        self.assertTrue(len(cmp_recs) == len(users))
        self.assertTrue(len(exp_recs) == len(users))
        self.assertTrue(len(int_recs) == len(users))
        for n in range(self.N_USERS):
            # У одного юзера три разных рекомендации
            triplet = (cmp_recs[n], exp_recs[n], int_recs[n])
            self.assertTrue(len(set([x.user for x in triplet])) == 1)
            self.assertTrue(len(set([x.item for x in triplet])) == 3)

    def test_restricted_generation(self):
        users = Student.objects.all()
        recom = TripleNetworkingRecommender(items_space=users)
        users = [users[0]]
        cmp_recs, exp_recs, int_recs = recom.get_recommendations(users=users)
        self.assertTrue(len(cmp_recs) == 1)
        self.assertTrue(len(exp_recs) == 1)
        self.assertTrue(len(int_recs) == 1)

    def test_staff_recommendations(self):
        users = Student.objects.all()
        recom = TripleNetworkingRecommender(items_space=users)
        cmp_recs, exp_recs, int_recs = recom.get_recommendations()
        staff_user = cmp_recs[0].item
        staff_user.is_staff = True
        staff_user.save()
        cmp_recs, exp_recs, int_recs = recom.get_recommendations()
        self.assertTrue(staff_user not in set(x.item for x in cmp_recs))
        self.assertTrue(staff_user not in set(x.item for x in exp_recs))
        self.assertTrue(staff_user not in set(x.item for x in int_recs))

        self.assertTrue(staff_user in set(x.user for x in cmp_recs))
        self.assertTrue(staff_user in set(x.user for x in exp_recs))
        self.assertTrue(staff_user in set(x.user for x in int_recs))
