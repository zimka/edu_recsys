from django.urls import path
from .api import ActivityRecommendationView

app_name = 'activity'

urlpatterns = [
    path('', ActivityRecommendationView.as_view()),
]
