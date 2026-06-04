"""
تكوين WSGI لمشروع شاليه النرجس
WSGI config for narjis_chalet project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narjis_chalet.settings')

application = get_wsgi_application()
