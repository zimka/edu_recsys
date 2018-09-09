from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import NetworkingRecommendation
from .serializer import NetworkingRecommendationSerializer


class NetworkRecommendationViewset(ReadOnlyModelViewSet):
    queryset = NetworkingRecommendation.objects.all()
    serializer_class = NetworkingRecommendationSerializer
    lookup_field = 'user__uid'

