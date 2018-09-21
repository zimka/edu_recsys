from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.core.api_utils import ApiKeyPermission
from .api_utils import ActivityRecommendationSerializer
from .models import ActivityRecommendation


class ActivityRecommendationViewset(ReadOnlyModelViewSet):
    serializer_class = ActivityRecommendationSerializer
    permission_classes = ApiKeyPermission,
    lookup_field = 'user__uid'
    queryset = ActivityRecommendation.objects.all()
