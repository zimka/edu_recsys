from apps.core.api_utils import RecommendationSerializer


class ActivityRecommendationSerializer(RecommendationSerializer):
    def get_item(self, obj):
        return obj.item.get_uid()