import json

from rest_framework import serializers

from edu_coresys.api_utils import StudentSerializer
from edu_coresys.models import Student
from .models import SingleScoreComputeTask


class SingleScoreComputeTaskSerializer(serializers.ModelSerializer):
    user = StudentSerializer(read_only=False)

    class Meta:
        model = SingleScoreComputeTask
        fields = ("uuid", 'user', 'input', 'output', 'complete', 'created')
        read_only_fields = ('uuid', 'output', 'complete', 'created')
        depth = 1

    def create(self, validated_data):
        user = validated_data.pop("user")
        student, created = Student.objects.get_or_create(**user)
        input = validated_data.pop('input', '{}')
        if isinstance(input, str):
            try:
                input = json.loads(input)
            except ValueError:
                input = None

        obj = SingleScoreComputeTask.objects.create(user=student, input=input)
        obj.compute_async()
        return obj