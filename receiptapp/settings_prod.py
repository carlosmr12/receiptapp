# Production settings for receiptapp

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE PRODUCTION SETTINGS ---
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['.run.app']
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# CSRF trusted origins are required for POST requests (e.g., admin login) over HTTPS.
# Wildcards are supported for subdomains.
CSRF_TRUSTED_ORIGINS = ['https://*.run.app']
if CUSTOM_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f'https://{CUSTOM_DOMAIN}')

# Cloud Run terminates SSL and forwards the original protocol in this header.
# This tells Django the request is secure.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'receipts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'storages', # Add storages for GCS
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'receiptapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'receiptapp.wsgi.application'

# --- PRODUCTION DATABASE ---
db_config = dj_database_url.parse(os.environ['DATABASE_URL'])
if os.environ.get('PROXY_RUN'):
    db_config['HOST'] = 'localhost'
    db_config['PORT'] = 5432
else:
    db_config['SSL_REQUIRE'] = True
db_config['CONN_MAX_AGE'] = 600
DATABASES = {'default': db_config}

# --- PRODUCTION STATIC & MEDIA FILES ---
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'

STORAGES = {
    # Uploaded files (receipt images) go to GCS under the 'media/' prefix
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": GS_BUCKET_NAME,
            "default_acl": "publicRead",
            "location": "media",
        },
    },
    # Static files (CSS/JS) go to GCS under the 'static/' prefix
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": GS_BUCKET_NAME,
            "default_acl": "publicRead",
            "location": "static",
        },
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Session timeout settings
SESSION_COOKIE_AGE = 2 * 60 * 60  # 2 hours
SESSION_SAVE_EVERY_REQUEST = True
