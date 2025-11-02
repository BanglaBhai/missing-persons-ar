# config/settings_prod.py
from .settings import *  # noqa

import os
DEBUG = False

# Hosts & security
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files with Whitenoise
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
] + MIDDLEWARE  # prepend these before the rest from base settings

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
WHITENOISE_USE_FINDERS = True

# CORS/CSRF from env
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS","").split(",") if o.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS","").split(",") if o.strip()]

# Database from DATABASE_URL
import dj_database_url
DATABASES = {
    "default": dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# (Optional) Media in demo mode (Render disk is ephemeral)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
