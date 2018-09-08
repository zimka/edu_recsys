import coreapi, coreschema
from rest_framework.schemas import AutoSchema

import logging


from rest_framework.schemas import AutoSchema
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apps.core.api_utils import ApiKeyPermission

from .models import SingleScoreComputeTask
from .serializer import SingleScoreComputeTaskSerializer

log = logging.getLogger(__name__)


class SingleScoreComputeTaskViewset(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.ListModelMixin,
                                    GenericViewSet):
    """
    Создание и чтение задач интерпретации
    """

    schema = AutoSchema()
    base_name = "single_score"
    permission_classes = ApiKeyPermission,
    serializer_class = SingleScoreComputeTaskSerializer

    def get_queryset(self):
        uid = self.request.query_params.get("user_uid")
        if uid:
            return SingleScoreComputeTask.objects.filter(user__uid=uid)
        else:
            return SingleScoreComputeTask.objects.all()
