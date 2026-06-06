"""
WSGI project for receiptapp.
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receiptapp.settings')

if os.environ.get('IS_MIGRATING') == 'true':
    execute_from_command_line(['manage.py', 'migrate'])
elif os.environ.get('IS_COLLECTING_STATIC') == 'true':
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
else:
    application = get_wsgi_application()
