from django.urls import path
from .views import DietPlanAPIView

urlpatterns = [
    path("plan/", DietPlanAPIView.as_view(), name="analyze-food"),
]