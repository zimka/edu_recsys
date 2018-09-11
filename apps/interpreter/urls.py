from rest_framework import routers
from django.urls import path, include
from .api import SingleScoreComputeTaskViewset

router = routers.SimpleRouter()
router.register(r'single_score', SingleScoreComputeTaskViewset, base_name="smth")


app_name = 'interpreteur'


urlpatterns = router.urls
