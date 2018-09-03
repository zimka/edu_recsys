from django.urls import path
from .api import UserDiagnosticsResultView

app_name = 'digital_profile'

urlpatterns = [
    path('<uuid:user_uuid>/', UserDiagnosticsResultView.as_view()),
]
