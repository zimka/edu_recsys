import uuid
from datetime import datetime
import pytz
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.schemas import AutoSchema
from rest_framework.pagination import LimitOffsetPagination
from apps.core.api_utils import RecommendationSerializer, ApiKeyPermission
import coreapi
import coreschema
from .manager import ActivityRecommendationManager


class ActivityRecommendationView(ListAPIView):
    """
    Текущие рекомендации по активностям

    **Пример**

        GET /api/v0/activity/fresh/?created_after=%Y-%m-%dT%H:%M:%S&user_uuid=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    **Response**

        * count: int

        * next: url

        * previous: url

        * results: list

            * user: uuid

            * activity: uuid

            * score: float 0-1

            * created: %Y-%m-%dT%H:%M:%S
    """
    serializer_class = RecommendationSerializer
    permission_classes = (ApiKeyPermission,)
    pagination_class = LimitOffsetPagination
    title = "Some activity recs"
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "created_after",
                location="query",
                required=False,
                schema=coreschema.String(
                    title="created_after",
                    description="Filter by creation datetime (%Y-%m-%dT%H:%M:%S)"
                ),
            ),
            coreapi.Field(
                "user_uuid",
                location="query",
                required=False,
                schema=coreschema.String(
                    title="user_uuid",
                    description="Filter by specific user uuid"
                ),
            ),
        ]
    )

    def get_queryset(self):
        created_after = self.request.query_params.get("created_after")
        if created_after:
            created_after = datetime.strptime(created_after, settings.DATETIME_FORMAT)
            if isinstance(created_after, datetime):
                created_after.replace(tzinfo=pytz.utc)
        user_uuid = self.request.query_params.get("user_uuid")
        try:
            if user_uuid is not None:
                user_uuid = uuid.UUID(user_uuid)
        except ValueError:
            raise ParseError("Invalid user_uuid format")
        return ActivityRecommendationManager().get_recommendations(created_after, user_uuid)
