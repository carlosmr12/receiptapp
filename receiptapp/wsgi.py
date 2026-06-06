"""
WSGI project for receiptapp.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receiptapp.settings')

application = get_wsgi_application()
