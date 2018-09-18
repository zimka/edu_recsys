import logging
from django.conf import settings
from rest_framework import serializers, permissions


log = logging.getLogger(__name__)


class RecommendationSerializer(serializers.Serializer):
    """
    Сериализатор для сырых рекомендаций
    """
    user = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    score = serializers.FloatField()
    created = serializers.DateTimeField(format=settings.DATETIME_FORMAT)

    def get_user(self, obj):
        return str(obj.user.get_uid())

    def get_item(self, obj):
        return str(obj.item)


class ApiKeyPermission(permissions.BasePermission):
    """
    Разрешение по X-Api-Key в хедере
    """

    def has_permission(self, request, view):
        api_key = getattr(settings, 'API_KEY', None)
        if not api_key:
            logging.error('API_KEY not configured')
        if api_key is False:
            return True

        key = request.META.get('HTTP_X_API_KEY')
        if key and api_key and key == api_key:
            return True
        return False