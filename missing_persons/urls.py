# missing_persons/urls.py
from django.urls import path
from .views import health

urlpatterns = [
    path("health/", health),  # ✅ GET /api/health/
]
