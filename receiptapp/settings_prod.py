# Import all settings from the base settings file
from .settings import *

# --- PRODUCTION STATIC FILES OVERRIDE ---
# This configuration is used by the collectstatic command in the CI/CD pipeline.

# Get the bucket name from the environment variable.
# This is fetched from GCP Secret Manager in the deploy.yml workflow.
GCS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')

if GCS_BUCKET_NAME:
    # Tell django-storages to use the GCS backend
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

    # Set the name of the bucket for django-storages
    GS_BUCKET_NAME = GCS_BUCKET_NAME

    # Set the default ACL to public-read so files are accessible
    GS_DEFAULT_ACL = 'publicRead'

    # Set the URL to serve static files from
    STATIC_URL = f'https://storage.googleapis.com/{GCS_BUCKET_NAME}/static/'
else:
    # If the bucket name isn't set, fail loudly during deployment.
    raise Exception("GS_BUCKET_NAME environment variable not set for production settings.")
