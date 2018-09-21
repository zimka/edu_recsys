from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField()

    class Meta:
        model = Student
        exclude = ("id", "leader_id", "is_removed")
