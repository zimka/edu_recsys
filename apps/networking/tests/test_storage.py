from django.test import TestCase

from edu_coresys.models import Student
from apps.core.tests import create_test_user
from apps.networking.models import InterestNetworkingRecommendation, \
    CompetenceNetworkingRecommendation, ExperienceNetworkingRecommendation
from apps.networking.recommender import TripleNetworkingRecommender


class ModelTest(TestCase):
    N_USERS = 5

    def setUp(self):
        for n in range(self.N_USERS):
            create_test_user(n)

    def test_recommendations_save(self):
        users = Student.objects.all()
        recom = TripleNetworkingRecommender(items_space=users)
        cmp_recs, exp_recs, int_recs = recom.get_recommendations()
        CompetenceNetworkingRecommendation.put_many(cmp_recs)
        ExperienceNetworkingRecommendation.put_many(exp_recs)
        InterestNetworkingRecommendation.put_many(int_recs)
        self.assertTrue(CompetenceNetworkingRecommendation.objects.count() == self.N_USERS)
        self.assertTrue(InterestNetworkingRecommendation.objects.count() == self.N_USERS)
        self.assertTrue(ExperienceNetworkingRecommendation.objects.count() == self.N_USERS)

    def test_recommendations_overwrite(self):
        users = Student.objects.all()
        recom = TripleNetworkingRecommender(items_space=users)
        cmp_recs, exp_recs, int_recs = recom.get_recommendations()
        CompetenceNetworkingRecommendation.put_many(cmp_recs)
        InterestNetworkingRecommendation.put_many(int_recs)
        ExperienceNetworkingRecommendation.put_many(exp_recs)

        staff_users = cmp_recs[0].user, cmp_recs[0].item
        for s in staff_users:
            s.is_staff = True
            s.save()

        cmp_recs, exp_recs, int_recs = recom.get_recommendations()
        CompetenceNetworkingRecommendation.put_many(cmp_recs)
        InterestNetworkingRecommendation.put_many(int_recs)
        ExperienceNetworkingRecommendation.put_many(exp_recs)

        self.assertTrue(CompetenceNetworkingRecommendation.objects.count() == self.N_USERS)
        self.assertTrue(InterestNetworkingRecommendation.objects.count() == self.N_USERS)
        self.assertTrue(ExperienceNetworkingRecommendation.objects.count() == self.N_USERS)
