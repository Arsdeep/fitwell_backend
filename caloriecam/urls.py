from django.urls import path
from .views import FoodCalorieAPIView, FoodSearchAPIView

urlpatterns = [
    path("analyze/", FoodCalorieAPIView.as_view(), name="analyze-food"),
    path("search/", FoodSearchAPIView.as_view(), name="search-food"),
]
