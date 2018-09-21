from django.urls import path, include
from rest_framework import routers

from .api import SingleScoreComputeTaskViewset

router = routers.SimpleRouter()
router.register(r'single_score', SingleScoreComputeTaskViewset, base_name="smth")


app_name = 'interpreteur'


urlpatterns = [
    path("inter/", include(router.urls)),
]
