import coreapi
import coreschema

from rest_framework.views import APIView, Response
from rest_framework.schemas import AutoSchema

from apps.core.api_utils import ApiKeyPermission
from apps.context.models import IsleContext, Student

from .models import UserDiagnosticsResults


class UserDiagnosticsResultView(APIView):
    """
    Прием данных диагностики из других источников
    """
    permission_classes = ApiKeyPermission,

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "context",
                location="body",
                required=True,
                schema=coreschema.String(
                    title="context",
                    description="Island context"
                ),
            ),
            coreapi.Field(
                "result",
                location="body",
                required=True,
                schema=coreschema.String(
                    title="context",
                    description="Diagnostics result"
                ),
            ),
        ]
    )

    def post(self, request, user_uuid):
        isle_context = IsleContext.get_from_name(request.data.get("context"))
        if not isle_context:
            isle_context = IsleContext.get_default()

        student, created = Student.objects.get_or_create(uuid=user_uuid)
        data = request.data.get('result')
        udr, created = UserDiagnosticsResults.objects.get_or_create(user=student, context=isle_context)
        udr.data = data
        udr.save()
        udr.build_profile()
        return Response(status=200)