# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Optional branding (won't affect routing)
admin.site.site_header = "Missing Persons Admin"
admin.site.site_title = "Missing Persons Admin"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path("admin/", admin.site.urls),                 # ✅ Admin
    path("api/", include("missing_persons.urls")),   # ✅ App API
]

# Serve media (fine for demo on Render)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
