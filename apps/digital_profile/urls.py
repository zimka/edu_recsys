from django.urls import path
from .api import UserDiagnosticsResultView, DigitalProfileView

app_name = 'digital_profile'

urlpatterns = [
    path('diagnostics/<uuid:user_uuid>', UserDiagnosticsResultView.as_view()),
    path('profile/<uuid:user_uuid>', DigitalProfileView.as_view()),

]
