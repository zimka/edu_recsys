from django.urls import path, include
from rest_framework import routers

from .api import InterestNetworkingRecommendationViewset, CompetenceNetworkingRecommendationViewset, \
    ExperienceNetworkingRecommendationViewset, CombinedNetworkingRecommendationView

router = routers.SimpleRouter()
router.register(r'competence', CompetenceNetworkingRecommendationViewset, base_name="networking_competence")
router.register(r'interests', InterestNetworkingRecommendationViewset, base_name="networking_interest")
router.register(r'experience', ExperienceNetworkingRecommendationViewset, base_name="networking_experience")


app_name = 'networking'


urlpatterns = [
    path("networking/<int:user__uid>/", CombinedNetworkingRecommendationView.as_view()),
    path("networking/", include(router.urls))
]
