"""
تكوين تطبيق الشاليه
Chalet app configuration
"""
from django.apps import AppConfig


class ChaletConfig(AppConfig):
    """تكوين تطبيق الشاليه - Chalet App Configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chalet'
    verbose_name = 'إدارة الشاليه'  # اسم التطبيق بالعربي
