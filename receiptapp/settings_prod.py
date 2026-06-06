# Production settings for receiptapp

import os
import dj_database_url
from pathlib import Path

print("--- LOADING settings_prod.py ---")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE PRODUCTION SETTINGS ---
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['.a.run.app']
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# Application definition
INSTALLED_APPS = [
    'receipts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages', # Add storages for GCS
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

# --- PRODUCTION STATIC FILES ---
print("--- CONFIGURING PRODUCTION STATICS ---")
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
GS_DEFAULT_ACL = 'publicRead'

print(f"--- STATICFILES_STORAGE set to: {STATICFILES_STORAGE} ---")
print(f"--- GS_BUCKET_NAME is: {GS_BUCKET_NAME} ---")

# --- MEDIA FILES (if needed in prod) ---
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

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