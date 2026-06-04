#!/usr/bin/env python
"""
ملف إدارة Django لمشروع شاليه النرجس
Django's command-line utility for administrative tasks.
"""
import os
import sys


def main():
    """تشغيل المهام الإدارية - Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'narjis_chalet.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "تعذر استيراد Django. تأكد من تثبيته وتفعيل البيئة الافتراضية. "
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
