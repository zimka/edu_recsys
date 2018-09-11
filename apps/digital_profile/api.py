import logging
import json
import coreapi
import coreschema

from rest_framework.views import APIView, Response
from rest_framework.schemas import AutoSchema

from apps.core.api_utils import ApiKeyPermission
from apps.context.models import IsleContext, Student

from .models import UserDiagnosticsResults, DigitalProfile

log = logging.getLogger(__name__)


class UserDiagnosticsResultView(APIView):
    """
    Прием данных диагностики из других источников.
    """
    permission_classes = ApiKeyPermission,

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "context",
                location="form",
                required=True,
                schema=coreschema.String(
                    title="context",
                    description="Island context"
                ),
            ),
            coreapi.Field(
                "data",
                location="form",
                required=True,
                type='json',
                schema=coreschema.String(
                    title="data",
                    description="Diagnostics data"
                ),
            ),
        ]
    )

    def post(self, request, user_uid):
        isle_context = IsleContext.get_from_name(request.data.get("context"))
        if not isle_context:
            isle_context = IsleContext.get_default()
        if not isle_context:
           return Response({"detail": "Unknown context"}, status=400)
        student = Student.get(uid=user_uid, create=True)
        data = request.data.get('data')

        if not isinstance(data, dict):
            try:
                data = json.loads(data)
            except ValueError as e:
                log.info("Error diagnostics create {}: {}".format(student.uuid, str(e)))
                return Response({"detail": "Data must be json"}, status=400)
        udr, created = UserDiagnosticsResults.objects.get_or_create(user=student, context=isle_context)
        udr.data = data
        udr.save()
        udr.build_profile()
        return Response(status=200)


class DigitalProfileView(APIView):
    """
    Доступ к рассчитанному цифровому профилю
    """
    permission_classes = ApiKeyPermission,
    schema = AutoSchema()

    def get(self, request, user_uid):
        try:
            student = Student.get(uid=user_uid)
        except Student.DoesNotExist:
            return Response({"detail": "Invalid user uuid"}, status=400)

        try:
            dp = DigitalProfile.objects.get(user=student)
        except DigitalProfile.DoesNotExist:
            return Response({"detail": "Not Ready"}, status=202)

        return Response(dp.get_serial(), status=200)
