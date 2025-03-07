from django.urls import path
from .views import FoodCalorieAPIView

urlpatterns = [
    path("analyze/", FoodCalorieAPIView.as_view(), name="analyze-food"),
]
