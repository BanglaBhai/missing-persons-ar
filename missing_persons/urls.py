# missing_persons/urls.py
from django.urls import path
from django.http import JsonResponse
from django.conf import settings
from django.urls import get_resolver

def health(_):
    return JsonResponse({"status": "ok"})

def debug(_):
    # What settings and URL patterns are actually active?
    resolver = get_resolver()
    patterns = [str(p.pattern) for p in resolver.url_patterns]
    return JsonResponse({
        "ROOT_URLCONF": settings.ROOT_URLCONF,
        "DEBUG": settings.DEBUG,
        "INSTALLED_APPS_has_admin": "django.contrib.admin" in settings.INSTALLED_APPS,
        "URL_patterns": patterns,  # You should see 'admin/' in here
    })

urlpatterns = [
    path("health/", health),  # GET /api/health/
    path("debug/", debug),    # GET /api/debug/
]
