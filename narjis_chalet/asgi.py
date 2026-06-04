"""
تكوين ASGI لمشروع شاليه النرجس
ASGI config for narjis_chalet project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narjis_chalet.settings')

application = get_asgi_application()
