"""
إعدادات Django لمشروع شاليه النرجس
Django settings for narjis_chalet project.
"""

from pathlib import Path
import os

# المسار الأساسي للمشروع - Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# مفتاح الأمان - Secret Key (غيّره في الإنتاج)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-narjis-chalet-2024-change-this-in-production'

# وضع التطوير - Debug mode (أوقفه في الإنتاج)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  #  ملاحظة هامة جداً قبل الإطلاق النهائي للجمهور: عند رفع الموقع على الاستضافة، تأكد من الدخول إلى ملف narjis_chalet/settings.py وتغيير سطر DEBUG = True إلى DEBUG = False. هذا الإجراء ضروري جداً لحماية موقعك وعدم إظهار أكواد الأخطاء للمستخدمين العاديين.
# المضيفين المسموح بهم - Allowed Hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pythonanywhere.com']


# التطبيقات المثبتة - Installed Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # تطبيقات المشروع - Project Apps
    'chalet.apps.ChaletConfig',
]

# البرمجيات الوسيطة - Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# تكوين الروابط - URL Configuration
ROOT_URLCONF = 'narjis_chalet.urls'

# إعدادات القوالب - Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'chalet.context_processors.site_settings',
            ],
        },
    },
]

# تطبيق WSGI
WSGI_APPLICATION = 'narjis_chalet.wsgi.application'


# قاعدة البيانات - Database
# استخدام SQLite للتطوير
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# إعدادات PostgreSQL (للإنتاج)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'narjis_chalet_db',
#         'USER': 'your_username',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# التحقق من كلمات المرور - Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# إعدادات اللغة والمنطقة الزمنية - Internationalization
# اللغة العربية
LANGUAGE_CODE = 'ar'

# المنطقة الزمنية - بغداد
TIME_ZONE = 'Asia/Baghdad'

# تفعيل الترجمة
USE_I18N = True

# تفعيل التوطين
USE_L10N = True

# استخدام المنطقة الزمنية
USE_TZ = True

# اللغات المتاحة
LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

# مسار ملفات الترجمة
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# الملفات الثابتة - Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ملفات الوسائط - Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# نوع المفتاح الأساسي الافتراضي - Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# إعدادات الرسائل - Messages Settings
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Fix for Windows CSS MIME type issue
import mimetypes
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)
