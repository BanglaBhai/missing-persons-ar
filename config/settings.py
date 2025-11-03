import os
from pathlib import Path
from datetime import timedelta

# ------------------------------------------------
# BASE DIRECTORIES
# ------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------
# SECURITY
# ------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key-for-dev")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "missing-persons-ar-backend.onrender.com",
]

# ------------------------------------------------
# APPLICATIONS
# ------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",          # ✅ Required for admin panel
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "corsheaders",
    # Local apps
    "missing_persons",
]

# ------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",  # ✅ For APPEND_SLASH
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------------------------
# URLS & WSGI
# ------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------
# DATABASE
# ------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "render"),
        "USER": os.environ.get("DB_USER", "render"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "missing-persons-db.onrender.com"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# ------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------
# STATIC & MEDIA
# ------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------
# CORS (for your frontend / Vercel)
# ------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ------------------------------------------------
# REST FRAMEWORK CONFIG
# ------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# ------------------------------------------------
# MISC SETTINGS
# ------------------------------------------------
APPEND_SLASH = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
