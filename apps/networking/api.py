from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.core.api_utils import ApiKeyPermission
from .models import NetworkingRecommendation
from .serializer import NetworkingRecommendationSerializer


class NetworkRecommendationViewset(ReadOnlyModelViewSet):
    queryset = NetworkingRecommendation.objects.all()
    serializer_class = NetworkingRecommendationSerializer
    permission_classes = ApiKeyPermission,
    lookup_field = 'user__uid'

