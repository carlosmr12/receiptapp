# Import all settings from the base settings file
from .settings import *
import os

# --- UNCONDITIONAL PRODUCTION STATIC FILES OVERRIDE ---
# This configuration is used by the collectstatic command in the CI/CD pipeline.

# Tell django-storages to use the GCS backend.
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Get the bucket name from the environment variable.
# This is fetched from GCP Secret Manager in the deploy.yml workflow.
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')

# Set the default ACL to public-read so files are accessible.
GS_DEFAULT_ACL = 'publicRead'

# Set the URL to serve static files from.
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
