from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.core.api_utils import ApiKeyPermission
from .models import NetworkingRecommendationDeprecated
from .serializer import NetworkingRecommendationSerializer


class NetworkRecommendationViewset(ReadOnlyModelViewSet):
    queryset = NetworkingRecommendationDeprecated.objects.all()
    serializer_class = NetworkingRecommendationSerializer
    permission_classes = ApiKeyPermission,
    lookup_field = 'user__uid'

