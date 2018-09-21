import json
from rest_framework import serializers
from apps.context.serializers import StudentSerializer
from apps.core.api_utils import RecommendationSerializer


class NetworkingRecommendationSerializer(RecommendationSerializer):
    def get_item(self, obj):
        return obj.item.get_uid()


class CombinedNetworkingRecommendationSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField('user')
    recommendations = serializers.SerializerMethodField('recommendations')

    FORMAT_MAP = {
        "cmp": "coffee",
        "exp": "discuss",
        "int": "look"
    }

    def get_user(self, obj):
        users_set = set(v.user for v in obj.values())
        if len(users_set) == 1:
            raise ValueError("Bad serializer usage")
        return StudentSerializer(list(users_set)[0])

    def get_recommendations(self, obj):
        data = []
        for k,v in obj.items():
            type = self.FORMAT_MAP[k]
            data.append({
                "target_ids": list(v.item.uid),
                "type": type
            })
        return json.dumps({"communication": data})
