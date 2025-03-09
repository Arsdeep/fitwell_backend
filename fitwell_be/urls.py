from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chatbot/", include("chatbot.urls")),
    path("calorie/", include("caloriecam.urls")),
    path("diet/", include("dietplan.urls")),
]
