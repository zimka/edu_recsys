from django.urls import path
from .api import UserDiagnosticsResultView, DigitalProfileView

app_name = 'digital_profile'

urlpatterns = [
    path('diagnostics/<int:user_uid>', UserDiagnosticsResultView.as_view()),
    path('profile/<int:user_uid>', DigitalProfileView.as_view()),

]
