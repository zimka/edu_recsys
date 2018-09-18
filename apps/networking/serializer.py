from rest_framework import serializers
from apps.context.models import Student
from .models import NetworkingRecommendationDeprecated


class NestedStudentSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField()

    class Meta:
        model = Student
        exclude = ("id", "leader_id", "is_removed")


class NetworkingRecommendationSerializer(serializers.ModelSerializer):
    user = NestedStudentSerializer(read_only=False)

    class Meta:
        model = NetworkingRecommendationDeprecated
        fields = ('user', 'recommendations', 'created')
        read_only_fields = fields
        depth = 1
