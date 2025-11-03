# config/urls.py
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def root_ping(_request):
    return HttpResponse("OK: root handler is alive")

urlpatterns = [
    path("", root_ping),                         # ✅ GET /
    path("admin/", admin.site.urls),             # ✅ GET /admin/
    path("api/", include("missing_persons.urls"))# ✅ GET /api/health/
]

# Serve media (fine for demo on Render)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
