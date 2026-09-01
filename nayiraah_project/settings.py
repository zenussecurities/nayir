import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# --------------------------------------------------------------------------
# Core / security
# --------------------------------------------------------------------------

# SECURITY WARNING: set a real, unique secret in production via the
# DJANGO_SECRET_KEY environment variable. This fallback is only for local
# development and is intentionally obviously insecure.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-only-change-me")

# DEBUG should be False in production (Vercel, Railway, etc)
# Set DJANGO_DEBUG=true only for local development
DEBUG = env_bool("DJANGO_DEBUG", default=False)

# ALLOWED_HOSTS configuration - automatically includes Vercel deployment domains
_allowed_hosts = env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,nayiraah.org,www.nayiraah.org"
)
_allowed_hosts.extend(["*", ".vercel.app", "vercel.app", "localhost", "127.0.0.1"])
_vercel_url = os.environ.get("VERCEL_URL", "").strip()
if _vercel_url:
    _allowed_hosts.append(_vercel_url)
    if not _vercel_url.startswith("."):
        _allowed_hosts.append(f".{_vercel_url}")

ALLOWED_HOSTS = list(set(_allowed_hosts))

# Site-wide constants used across templates and SEO tags (see
# core/context_processors.py). Update these for your real domain/handle.
SITE_NAME = "Nayi Raah"
SITE_TAGLINE = "Nova Vita, Nova Via — Turning ideas into skills and support into action."
SITE_DEFAULT_DESCRIPTION = (
    "Nayi Raah helps every girl across India bloom with confidence, courage "
    "and opportunity through education, wellness guidance and support."
)
SITE_DOMAIN = os.environ.get(
    "DJANGO_SITE_DOMAIN",
    "nayiraah.org"
)

# Build CSRF_TRUSTED_ORIGINS to include both custom domain and Vercel domains
_csrf_origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    f"https://{SITE_DOMAIN}",
    f"https://www.{SITE_DOMAIN}",
    "https://*.vercel.app",
    "https://*.now.sh",
]

if _vercel_url:
    _csrf_origins.append(f"https://{_vercel_url}")

_custom_origins = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "")
_csrf_origins.extend(_custom_origins)

CSRF_TRUSTED_ORIGINS = list(set(o for o in _csrf_origins if o))

SOCIAL_INSTAGRAM = "https://www.instagram.com/_nayiraah_/"

# Always trust Vercel/reverse proxy HTTPS header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", default=False)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
else:
    SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# --------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # efficient static file serving + caching headers
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nayiraah_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_meta",
            ],
        },
    },
]

WSGI_APPLICATION = "nayiraah_project.wsgi.application"


# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------
# SQLite by default (fine for a lightweight brochure-style site). Set
# DJANGO_DATABASE_URL-style env vars yourself and swap this block if you
# outgrow it and need Postgres.

# Use dj-database-url to read DATABASE_URL environment variable (for production)
# Falls back to SQLite for local development
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --------------------------------------------------------------------------
# Password validation
# --------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --------------------------------------------------------------------------
# Internationalization
# --------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------------
# Static & media files
# --------------------------------------------------------------------------
# WhiteNoise serves static files with far-future cache headers and (in
# production) pre-compresses them, keeping this Django-only stack fast
# without needing a separate nginx/CDN static layer for a small site.

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Uploaded images are re-encoded server-side on save where relevant, but keep
# an upper bound here too so a single bad upload can't exhaust disk/bandwidth.
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB


# --------------------------------------------------------------------------
# Email (used to notify admins of new contact-form messages)
# --------------------------------------------------------------------------

EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "")
# Safe conversion of EMAIL_PORT with fallback to 587
_email_port = os.environ.get("DJANGO_EMAIL_PORT", "587").strip()
EMAIL_PORT = int(_email_port) if _email_port else 587
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("DJANGO_EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", f"no-reply@{SITE_DOMAIN}")
ADMINS = [
    tuple(pair.split(":", 1))
    for pair in env_list("DJANGO_ADMINS", "")
    if ":" in pair
]


# --------------------------------------------------------------------------
# Caching
# --------------------------------------------------------------------------
# Local in-process cache is enough for a small, mostly-static site and needs
# no extra infrastructure. Swap LOCATION/BACKEND for Redis/Memcached only if
# you're running multiple app server processes and need a shared cache.

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "nayiraah-cache",
    }
}


# --------------------------------------------------------------------------
# Misc
# --------------------------------------------------------------------------

LOGIN_URL = "/admin/login/"


# --------------------------------------------------------------------------
# Logging (for debugging production issues)
# --------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}
