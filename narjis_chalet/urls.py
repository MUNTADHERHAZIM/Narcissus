"""
روابط URL الرئيسية لمشروع شاليه النرجس
Main URL configuration for narjis_chalet project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# تخصيص لوحة الإدارة - Customize Admin Site
admin.site.site_header = 'لوحة إدارة شاليه النرجس'
admin.site.site_title = 'شاليه النرجس'
admin.site.index_title = 'مرحباً بك في لوحة الإدارة'

urlpatterns = [
    # لوحة الإدارة - Admin Panel
    path('admin/', admin.site.urls),
    
    # روابط تطبيق الشاليه - Chalet App URLs
    path('', include('chalet.urls')),
]

# إضافة روابط الملفات الثابتة والوسائط في وضع التطوير
# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
