from rest_framework import serializers
from apps.context.models import Student
from .models import SingleScoreComputeTask


class NestedStudentSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField()

    class Meta:
        model = Student
        exclude = ("leader_id", "is_removed")


class SingleScoreComputeTaskSerializer(serializers.ModelSerializer):
    user = NestedStudentSerializer(read_only=False)

    class Meta:
        model = SingleScoreComputeTask
        fields = ("uuid", 'user', 'input', 'output', 'complete')
        read_only_fields = ('uuid', 'output', 'complete')
        depth = 1

    def create(self, validated_data):
        user = validated_data.pop("user")
        student, created = Student.objects.get_or_create(**user)
        return SingleScoreComputeTask.objects.create(user=student, **validated_data)
