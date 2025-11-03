# config/failsafe_urls.py
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, JsonResponse

def root(_):
    return HttpResponse("OK from failsafe root")

def health(_):
    return JsonResponse({"status": "ok", "from": "failsafe"})

urlpatterns = [
    path("", root),                 # GET /
    path("admin/", admin.site.urls),# GET /admin/
    path("api/health/", health),    # GET /api/health/
]
