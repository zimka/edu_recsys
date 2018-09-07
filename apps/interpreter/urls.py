from rest_framework import routers
from django.urls import path, include
from .api import SinlgleScoreComputeTaskViewset

router = routers.SimpleRouter()
router.register(r'single_score', SinlgleScoreComputeTaskViewset, base_name="smth")


app_name = 'interpreteur'


urlpatterns = router.urls
