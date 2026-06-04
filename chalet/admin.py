"""
إعدادات لوحة الإدارة لتطبيق الشاليه
Admin configuration for chalet app

يوفر:
- واجهة إدارة بالعربي
- فلاتر البحث والتصفية
- إجراءات تأكيد وإلغاء الحجوزات
- عرض الصور داخل النماذج
"""

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Chalet, ChaletImage, ChaletFeature, Booking, ContactMessage, Review, SiteSettings


class ChaletImageInline(admin.TabularInline):
    """
    عرض صور الشاليه داخل صفحة الشاليه
    Inline display of chalet images
    """
    model = ChaletImage
    extra = 1
    fields = ['image', 'caption', 'is_main', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """عرض معاينة الصورة"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url
            )
        return "لا توجد صورة"
    image_preview.short_description = 'معاينة'


class ChaletFeatureInline(admin.TabularInline):
    """
    عرض مميزات الشاليه داخل صفحة الشاليه
    Inline display of chalet features
    """
    model = ChaletFeature
    extra = 1
    fields = ['name', 'icon', 'description']


@admin.register(Chalet)
class ChaletAdmin(admin.ModelAdmin):
    """
    إعدادات صفحة إدارة الشاليهات
    Chalet Admin Configuration
    """
    list_display = [
        'name', 'location', 'price_per_night', 
        'max_guests', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'location', 'description']
    list_editable = ['is_active', 'price_per_night']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name', 'short_description', 'description', 'video', 'youtube_video')
        }),
        ('الموقع والسعر', {
            'fields': ('location', 'location_url', 'price_per_night', 'max_guests')
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ChaletImageInline, ChaletFeatureInline]


@admin.register(ChaletImage)
class ChaletImageAdmin(admin.ModelAdmin):
    """
    إعدادات صفحة إدارة صور الشاليه
    Chalet Image Admin Configuration
    """
    list_display = ['chalet', 'caption', 'is_main', 'order', 'image_preview', 'created_at']
    list_filter = ['chalet', 'is_main', 'created_at']
    search_fields = ['caption', 'chalet__name']
    list_editable = ['is_main', 'order']
    
    def image_preview(self, obj):
        """عرض معاينة الصورة"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px;" />',
                obj.image.url
            )
        return "لا توجد صورة"
    image_preview.short_description = 'معاينة'


@admin.register(ChaletFeature)
class ChaletFeatureAdmin(admin.ModelAdmin):
    """
    إعدادات صفحة إدارة مميزات الشاليه
    Chalet Feature Admin Configuration
    """
    list_display = ['name', 'chalet', 'icon', 'description']
    list_filter = ['chalet', 'icon']
    search_fields = ['name', 'description', 'chalet__name']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    إعدادات صفحة إدارة الحجوزات
    Booking Admin Configuration
    """
    list_display = [
        'id', 'name', 'chalet', 'check_in', 'check_out', 
        'guests', 'status_badge', 'total_price', 'created_at'
    ]
    list_filter = ['status', 'chalet', 'check_in', 'created_at']
    search_fields = ['name', 'email', 'phone', 'chalet__name']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('معلومات العميل', {
            'fields': ('name', 'email', 'phone')
        }),
        ('تفاصيل الحجز', {
            'fields': ('chalet', 'check_in', 'check_out', 'guests', 'notes')
        }),
        ('الحالة والسعر', {
            'fields': ('status', 'total_price')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['confirm_bookings', 'cancel_bookings', 'mark_completed']
    
    def status_badge(self, obj):
        """عرض حالة الحجز كشارة ملونة"""
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'cancelled': '#dc3545',
            'completed': '#17a2b8',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'الحالة'
    status_badge.admin_order_field = 'status'
    
    @admin.action(description='تأكيد الحجوزات المحددة')
    def confirm_bookings(self, request, queryset):
        """إجراء تأكيد الحجوزات"""
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'تم تأكيد {updated} حجز بنجاح')
    
    @admin.action(description='إلغاء الحجوزات المحددة')
    def cancel_bookings(self, request, queryset):
        """إجراء إلغاء الحجوزات"""
        updated = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(request, f'تم إلغاء {updated} حجز')
    
    @admin.action(description='وضع علامة مكتمل')
    def mark_completed(self, request, queryset):
        """إجراء وضع علامة مكتمل"""
        updated = queryset.filter(status='confirmed').update(status='completed')
        self.message_user(request, f'تم وضع علامة مكتمل على {updated} حجز')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    إعدادات صفحة إدارة رسائل الاتصال
    Contact Message Admin Configuration
    """
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    @admin.action(description='وضع علامة مقروءة')
    def mark_as_read(self, request, queryset):
        """وضع علامة مقروءة على الرسائل"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'تم وضع علامة مقروءة على {updated} رسالة')
    
    @admin.action(description='وضع علامة غير مقروءة')
    def mark_as_unread(self, request, queryset):
        """وضع علامة غير مقروءة على الرسائل"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'تم وضع علامة غير مقروءة على {updated} رسالة')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    إعدادات صفحة إدارة آراء العملاء
    Review Admin Configuration
    """
    list_display = ['customer_name', 'chalet', 'rating', 'is_active', 'created_at']
    list_filter = ['is_active', 'rating', 'chalet', 'created_at']
    search_fields = ['customer_name', 'comment']
    list_editable = ['is_active', 'rating']
    readonly_fields = ['created_at']


class SiteSettingsForm(forms.ModelForm):
    """نموذج لتخصيص حقول الإعدادات في لوحة الإدارة"""
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 80px; padding: 0; cursor: pointer;'}),
            'primary_dark_color': forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 80px; padding: 0; cursor: pointer;'}),
            'primary_light_color': forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 80px; padding: 0; cursor: pointer;'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 80px; padding: 0; cursor: pointer;'}),
            'secondary_dark_color': forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 80px; padding: 0; cursor: pointer;'}),
            'secondary_light_color': forms.TextInput(attrs={'type': 'color', 'style': 'height: 40px; width: 80px; padding: 0; cursor: pointer;'}),
        }

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    إعدادات صفحة إدارة الإعدادات العامة
    Site Settings Admin Configuration
    """
    form = SiteSettingsForm
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('site_name', 'site_description')
        }),
        ('معلومات الاتصال', {
            'fields': ('phone_number', 'whatsapp_number', 'email_address')
        }),
        ('الموقع', {
            'fields': ('location_text',)
        }),
        ('التواصل الاجتماعي', {
            'fields': ('facebook_url', 'instagram_url', 'telegram_url')
        }),
        ('الألوان (Theme)', {
            'fields': (
                'primary_color', 'primary_dark_color', 'primary_light_color',
                'secondary_color', 'secondary_dark_color', 'secondary_light_color'
            ),
            'description': 'انقر على مربع اللون لاختيار الألوان بكل سهولة (Color Picker).'
        }),
    )

    def has_add_permission(self, request):
        """منع إضافة أكثر من سجل واحد للإعدادات"""
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)

