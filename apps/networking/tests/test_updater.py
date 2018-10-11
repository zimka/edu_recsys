from django.test import TestCase

from recsys_base.tests import create_test_user, Student
from ..models import CompetenceNetworkingRecommendation, InterestNetworkingRecommendation, ExperienceNetworkingRecommendation
from ..updater import NetworkingRecommendationUpdater


class UpdaterTestCase(TestCase):
    N_USERS = 3

    def setUp(self):
        for n in range(self.N_USERS):
            create_test_user(n)

    def test_update_all(self):
        len_c = CompetenceNetworkingRecommendation.objects.count()
        len_e = ExperienceNetworkingRecommendation.objects.count()
        len_i = InterestNetworkingRecommendation.objects.count()
        self.assertFalse(len_c or len_e or len_i)

        updater = NetworkingRecommendationUpdater()
        updater.do_update()

        len_c = CompetenceNetworkingRecommendation.objects.count()
        len_e = ExperienceNetworkingRecommendation.objects.count()
        len_i = InterestNetworkingRecommendation.objects.count()
        self.assertTrue(len_c == self.N_USERS and len_e == self.N_USERS and len_i == self.N_USERS)

    def test_update_single(self):
        updater = NetworkingRecommendationUpdater()
        updater.do_update()
        student = Student.objects.first()

        old_c = CompetenceNetworkingRecommendation.objects.get(user=student)
        old_e = InterestNetworkingRecommendation.objects.get(user=student)
        old_i = ExperienceNetworkingRecommendation.objects.get(user=student)

        updater.do_single_update(student)

        new_c = CompetenceNetworkingRecommendation.objects.get(user=student)
        new_e = InterestNetworkingRecommendation.objects.get(user=student)
        new_i = ExperienceNetworkingRecommendation.objects.get(user=student)

        self.assertTrue(old_c!=new_c and old_e!=new_e and old_i!=new_i)
