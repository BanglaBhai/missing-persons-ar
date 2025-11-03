# missing_persons/urls.py
from django.urls import path
from django.http import JsonResponse

def health(_request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("health/", health),   # GET /api/health/ returns {"status":"ok"}
]
