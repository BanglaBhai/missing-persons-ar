# config/settings_prod.py
from .settings import *  # base settings
import os
import dj_database_url

# ------------------------------------------------
# GENERAL
# ------------------------------------------------
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# Force this settings file to use the failsafe URLConf
ROOT_URLCONF = "config.failsafe_urls"

# Hosts and security
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ------------------------------------------------
# STATIC / MEDIA
# ------------------------------------------------
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
WHITENOISE_USE_FINDERS = True

# ------------------------------------------------
# DATABASE
# ------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        ssl_require=True,
        default=os.getenv("DATABASE_URL", "")
    )
}

# ------------------------------------------------
# CORS & CSRF
# ------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
]
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# ------------------------------------------------
# MIDDLEWARE (prepend critical ones)
# ------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
] + MIDDLEWARE

# ------------------------------------------------
# ENSURE ADMIN + CORE APPS EXIST
# ------------------------------------------------
required_admin_apps = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
for app in required_admin_apps:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.insert(0, app)

# ------------------------------------------------
# MISC
# ------------------------------------------------
APPEND_SLASH = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
