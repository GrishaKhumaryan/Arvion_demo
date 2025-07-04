# Arvion_demo/Arvion/settings.py (ՎԵՐՋՆԱԿԱՆ ՏԱՐԲԵՐԱԿ)

import os
from pathlib import Path
import dj_database_url
import cloudinary         # Միայն այս import-ն է պետք այստեղ
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Գաղտնի տվյալներ և հիմնական կարգավորումներ ---
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-!hu)b&ofry6yz)e7e3us_44#23*o8+!+9cbuzf83i4_d_l3agx")
DEBUG = os.environ.get("DEBUG", "0") == "1"
ALLOWED_HOSTS = ["arvion.onrender.com", "18.156.158.53", "localhost", "127.0.0.1"]

# --- Հավելվածների ցուցակ ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "main.apps.MainConfig",
    'cloudinary_storage', # Սա պետք է լինի
    'cloudinary',       # Սա պետք է լինի
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Arvion.urls"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Arvion.wsgi.application"

# --- Տվյալների բազա ---
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# --- Ավտորիզացիա ---
AUTH_USER_MODEL = 'main.CustomUser'
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Լեզու և ժամանակ ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- API Keys ---
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

# ==============================================================================
# CLOUDINARY-Ի ԿԱՐԳԱՎՈՐՈՒՄՆԵՐ (ՄԻԱԿ ՃԻՇՏ ՏԵՂԸ)
# ==============================================================================
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', "dhofwkbdd"),
    api_key=os.environ.get('CLOUDINARY_API_KEY', "716419361996157"),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', "JoS5_jjjng6JKcpF3mWnQw2STAI"),
    secure=True
)

# Django-ին հրահանգում ենք, որ media ֆայլերի համար օգտագործի Cloudinary-ն։
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ==============================================================================
# STATIC & MEDIA ՖԱՅԼԵՐ
# ==============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Երբ օգտագործում ենք Cloudinary, MEDIA_ROOT-ը production-ում այլևս էական չէ,
# բայց այն կարևոր է լոկալ միջավայրում աշխատանքի համար։
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"