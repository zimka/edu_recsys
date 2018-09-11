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

        GET /api/v0/activity/fresh/?created_after=%Y-%m-%dT%H:%M:%S&user_uid=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    **Response**

        * count: int

        * next: url

        * previous: url

        * results: list

            * user: uid(int)

            * activity: uid

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
                "user",
                location="query",
                required=False,
                schema=coreschema.String(
                    title="user",
                    description="Filter by specific user uid"
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
        uid = self.request.query_params.get("user")
        try:
            if uid is not None:
                uid = int(uid)
        except ValueError:
            raise ParseError("Invalid uid format")
        return ActivityRecommendationManager().get_recommendations(created_after, uid)
