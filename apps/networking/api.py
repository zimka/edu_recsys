from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.core.api_utils import ApiKeyPermission
from .api_utils import NetworkingRecommendationSerializer, CombinedNetworkingRecommendationSerializer
from .models import CompetenceNetworkingRecommendation, InterestNetworkingRecommendation, \
    ExperienceNetworkingRecommendation


class BaseNetworkRecommendationViewset(ReadOnlyModelViewSet):
    serializer_class = NetworkingRecommendationSerializer
    permission_classes = ApiKeyPermission,
    lookup_field = 'user__uid'


class CompetenceNetworkingRecommendationViewset(BaseNetworkRecommendationViewset):
    queryset = CompetenceNetworkingRecommendation.objects.all()


class InterestNetworkingRecommendationViewset(BaseNetworkRecommendationViewset):
    queryset = InterestNetworkingRecommendation.objects.all()


class ExperienceNetworkingRecommendationViewset(BaseNetworkRecommendationViewset):
    queryset = ExperienceNetworkingRecommendation.objects.all()


class CombinedNetworkingRecommendationView(RetrieveAPIView):
    permission_classes = ApiKeyPermission,
    serializer_class = CombinedNetworkingRecommendationSerializer

    def get_object(self):
        uid = self.kwargs['user__uid']
        filter = {"user__uid": uid}
        return {
            "cmp": get_object_or_404(CompetenceNetworkingRecommendation, **filter),
            "exp": get_object_or_404(ExperienceNetworkingRecommendation, **filter),
            "int": get_object_or_404(InterestNetworkingRecommendation, **filter),
        }
