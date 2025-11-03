# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),                 # ✅ Admin
    path("api/", include("missing_persons.urls")),   # ✅ Your API
]

# (OK for demo on Render so image fields work)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
