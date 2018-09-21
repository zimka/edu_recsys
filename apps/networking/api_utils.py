from rest_framework import serializers

from apps.context.api_utils import StudentSerializer
from apps.core.api_utils import RecommendationSerializer


class NetworkingRecommendationSerializer(RecommendationSerializer):
    def get_item(self, obj):
        return str(obj.item.get_uid())


class CombinedNetworkingRecommendationSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()

    FORMAT_MAP = {
        "cmp": "coffee",
        "exp": "discuss",
        "int": "look"
    }

    def get_user(self, obj):
        users_triple = set(v.user for v in obj.values())
        if len(users_triple) != 1:
            raise ValueError("Bad serializer usage")
        return StudentSerializer(list(users_triple)[0]).data

    def get_recommendations(self, obj):
        data = []
        for k,v in obj.items():
            type = self.FORMAT_MAP[k]
            data.append({
                'target_ids': [v.item.uid],
                'type': type
            })
        return {'communication': data}
