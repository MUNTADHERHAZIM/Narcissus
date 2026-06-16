"""
روابط URL لتطبيق الشاليه
URL patterns for chalet app
"""

from django.urls import path
from . import views

app_name = 'chalet'

urlpatterns = [
    # الصفحة الرئيسية - Home
    path('', views.home, name='home'),
    
    # معرض الصور - Gallery
    path('gallery/', views.gallery, name='gallery'),
    
    # تفاصيل الشاليه - Chalet Detail
    path('chalet/', views.chalet_detail, name='chalet_detail'),
    path('chalet/<int:pk>/', views.chalet_detail, name='chalet_detail_pk'),
    
    # الحجز - Booking
    path('booking/', views.booking, name='booking'),
    path('booking/<int:pk>/', views.booking, name='booking_pk'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    
    # اتصل بنا - Contact
    path('contact/', views.contact, name='contact'),
    
    # API للشفتات المحجوزة
    path('api/booked-shifts/<int:pk>/', views.check_shifts_availability, name='check_shifts_availability'),
    path('api/booked-dates/<int:pk>/', views.get_booked_dates, name='get_booked_dates'),
    
    # لوحة تحكم الإدارة - Admin Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/booking/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('dashboard/booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('dashboard/receipt/<int:booking_id>/', views.booking_receipt, name='booking_receipt'),
]
