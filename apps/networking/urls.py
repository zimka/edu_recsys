from rest_framework import routers
from .api import NetworkRecommendationViewset

router = routers.SimpleRouter()
router.register(r'', NetworkRecommendationViewset, base_name="networking")


app_name = 'networking'


urlpatterns = router.urls
