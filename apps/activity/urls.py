from django.urls import path, include
from rest_framework import routers

from .api import ActivityRecommendationViewset

router = routers.SimpleRouter()
router.register(r'', ActivityRecommendationViewset, base_name="activity")


app_name = 'activity'


urlpatterns = [
    path("activity/", include(router.urls))
]