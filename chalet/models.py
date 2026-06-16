"""
نماذج قاعدة البيانات لتطبيق الشاليه
Database models for chalet app

النماذج المتوفرة:
- Chalet: نموذج الشاليه الرئيسي
- ChaletImage: صور الشاليه
- ChaletFeature: مزايا الشاليه
- Booking: حجوزات الشاليه
"""

from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

# مدقق رقم الهاتف العراقي (11 رقماً يبدأ بـ 07)
phone_regex = RegexValidator(
    regex=r'^07[0-9]{9}$',
    message='أدخل رقم هاتف عراقي صحيح يتكون من 11 رقماً ويبدأ بـ 07. مثال: 07701234567'
)

class Chalet(models.Model):
    """
    نموذج الشاليه الرئيسي
    Main Chalet Model
    
    يحتوي على المعلومات الأساسية للشاليه مثل الاسم والوصف والموقع والسعر
    """
    
    name = models.CharField(
        max_length=200,
        verbose_name='اسم الشاليه',
        help_text='أدخل اسم الشاليه'
    )
    
    description = models.TextField(
        verbose_name='وصف الشاليه',
        help_text='أدخل وصفاً تفصيلياً للشاليه'
    )
    
    short_description = models.CharField(
        max_length=300,
        verbose_name='وصف مختصر',
        help_text='وصف مختصر يظهر في الصفحة الرئيسية',
        blank=True
    )
    
    location = models.CharField(
        max_length=300,
        verbose_name='الموقع',
        help_text='عنوان أو موقع الشاليه'
    )
    
    location_url = models.URLField(
        verbose_name='رابط الموقع على الخريطة',
        help_text='رابط Google Maps أو أي خريطة أخرى',
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to='chalet_videos/',
        verbose_name='فيديو تعريفي',
        blank=True,
        null=True,
        help_text='رفع فيديو تعريفي للشاليه (MP4, WebM, Ogg)'
    )

    youtube_video = models.URLField(
        verbose_name='رابط فيديو يوتيوب',
        help_text='أدخل رابط فيديو يوتيوب (مثال: https://www.youtube.com/watch?v=...)',
        blank=True,
        null=True
    )

    morning_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='سعر الشفت الصباحي',
        help_text='السعر بالدينار العراقي لشفت (8 صباحاً - 3 ظهراً)',
        validators=[MinValueValidator(0)],
        default=0
    )

    evening_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='سعر الشفت المسائي',
        help_text='السعر بالدينار العراقي لشفت (5 عصراً - 11 ليلاً)',
        validators=[MinValueValidator(0)],
        default=0
    )

    overnight_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='سعر شفت المبيت',
        help_text='السعر بالدينار العراقي لشفت (12 منتصف الليل - 6 صباحاً)',
        validators=[MinValueValidator(0)],
        default=0
    )
    
    max_guests = models.PositiveIntegerField(
        default=10,
        verbose_name='أقصى عدد نزلاء',
        help_text='الحد الأقصى لعدد النزلاء'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشط',
        help_text='هل الشاليه متاح للحجز؟'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    class Meta:
        verbose_name = 'شاليه'
        verbose_name_plural = 'الشاليهات'
        ordering = ['-created_at']
    
    def get_youtube_embed_url(self):
        """
        استخراج رابط التضمين من رابط يوتيوب
        Extract YouTube embed URL
        """
        if not self.youtube_video:
            return None
        
        # استخراج المعرف من الرابط
        import re
        
        # أنماط روابط يوتيوب المختلفة
        # youtube.com/watch?v=VIDEO_ID
        # youtube.com/embed/VIDEO_ID
        # youtu.be/VIDEO_ID
        
        regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(regex, self.youtube_video)
        
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        
        return self.youtube_video

    def __str__(self):
        return self.name
    
    def get_main_image(self):
        """الحصول على الصورة الرئيسية للشاليه"""
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image
        return self.images.first()
    
    def get_all_images(self):
        """الحصول على جميع صور الشاليه"""
        return self.images.all()
    
    def get_features(self):
        """الحصول على مزايا الشاليه"""
        return self.features.all()


class ChaletImage(models.Model):
    """
    نموذج صور الشاليه
    Chalet Images Model
    
    يسمح بإضافة صور متعددة لكل شاليه
    """
    
    chalet = models.ForeignKey(
        Chalet,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='الشاليه'
    )
    
    image = models.ImageField(
        upload_to='chalet_images/',
        verbose_name='الصورة'
    )
    
    caption = models.CharField(
        max_length=200,
        verbose_name='وصف الصورة',
        blank=True,
        help_text='وصف مختصر للصورة'
    )
    
    is_main = models.BooleanField(
        default=False,
        verbose_name='صورة رئيسية',
        help_text='هل هذه الصورة الرئيسية للشاليه؟'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='الترتيب',
        help_text='ترتيب ظهور الصورة'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإضافة'
    )
    
    class Meta:
        verbose_name = 'صورة الشاليه'
        verbose_name_plural = 'صور الشاليه'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"صورة {self.chalet.name} - {self.caption or 'بدون وصف'}"
    
    def save(self, *args, **kwargs):
        """التأكد من وجود صورة رئيسية واحدة فقط"""
        if self.is_main:
            # إلغاء تحديد الصور الرئيسية الأخرى
            ChaletImage.objects.filter(
                chalet=self.chalet,
                is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)


class ChaletFeature(models.Model):
    """
    نموذج مزايا الشاليه
    Chalet Features Model
    
    مثل: بركة سباحة، واي فاي، مطبخ، تكييف، إلخ
    """
    
    # أيقونات Font Awesome المتاحة
    ICON_CHOICES = [
        ('fa-swimming-pool', 'بركة سباحة'),
        ('fa-wifi', 'واي فاي'),
        ('fa-utensils', 'مطبخ'),
        ('fa-snowflake', 'تكييف'),
        ('fa-tv', 'تلفزيون'),
        ('fa-parking', 'موقف سيارات'),
        ('fa-bed', 'غرف نوم'),
        ('fa-bath', 'حمامات'),
        ('fa-tree', 'حديقة'),
        ('fa-fire', 'شواء/باربكيو'),
        ('fa-gamepad', 'ألعاب'),
        ('fa-child', 'ألعاب أطفال'),
        ('fa-shield-alt', 'أمن وحراسة'),
        ('fa-concierge-bell', 'خدمة الغرف'),
        ('fa-hot-tub', 'جاكوزي'),
        ('fa-umbrella-beach', 'مظلات'),
        ('fa-couch', 'غرفة معيشة'),
        ('fa-blender', 'أجهزة مطبخ'),
        ('fa-door-open', 'مدخل خاص'),
        ('fa-users', 'مجالس'),
    ]
    
    chalet = models.ForeignKey(
        Chalet,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='الشاليه'
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name='اسم الميزة',
        help_text='مثال: بركة سباحة، واي فاي'
    )
    
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='fa-check',
        verbose_name='الأيقونة',
        help_text='اختر أيقونة مناسبة للميزة'
    )
    
    description = models.CharField(
        max_length=200,
        verbose_name='وصف الميزة',
        blank=True,
        help_text='وصف إضافي للميزة (اختياري)'
    )
    
    class Meta:
        verbose_name = 'ميزة الشاليه'
        verbose_name_plural = 'مزايا الشاليه'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.chalet.name}"


class Booking(models.Model):
    """
    نموذج الحجوزات
    Booking Model
    
    يحتوي على جميع معلومات الحجز
    """
    
    # حالات الحجز
    STATUS_CHOICES = [
        ('pending', 'جديد - قيد المراجعة'),
        ('confirmed', 'مؤكد'),
        ('cancelled', 'ملغى'),
        ('completed', 'مكتمل'),
    ]
    
    # مدقق رقم الهاتف العراقي
    phone_regex = RegexValidator(
        regex=r'^07[0-9]{9}$',
        message='أدخل رقم هاتف عراقي صحيح يتكون من 11 رقماً ويبدأ بـ 07. مثال: 07701234567'
    )
    
    chalet = models.ForeignKey(
        Chalet,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='الشاليه'
    )
    
    # معلومات العميل
    name = models.CharField(
        max_length=100,
        verbose_name='الاسم الكامل',
        help_text='أدخل اسمك الكامل'
    )
    
    email = models.EmailField(
        verbose_name='البريد الإلكتروني',
        help_text='أدخل بريدك الإلكتروني (اختياري)',
        blank=True,
        null=True
    )
    
    phone = models.CharField(
        max_length=15,
        validators=[phone_regex],
        verbose_name='رقم الهاتف',
        help_text='أدخل رقم هاتفك. مثال: 07701234567'
    )
    
    # تفاصيل الحجز
    check_in = models.DateField(
        verbose_name='تاريخ الحجز',
        help_text='تاريخ الإقامة'
    )
    
    # الشفتات
    shift_morning = models.BooleanField(
        default=False,
        verbose_name='الصباحي (8 ص - 3 م)'
    )
    
    shift_evening = models.BooleanField(
        default=False,
        verbose_name='المسائي (5 م - 11 م)'
    )
    
    shift_overnight = models.BooleanField(
        default=False,
        verbose_name='المبيت (12 ل - 6 ص)'
    )

    # نوع المناسبة
    EVENT_CHOICES = [
        ('عائلية', 'عائلية'),
        ('شباب', 'شباب'),
        ('عيد ميلاد', 'عيد ميلاد'),
        ('حنة', 'حنة'),
        ('سفرة مدرسية', 'سفرة مدرسية'),
        ('حفل تخرج','حفل تخرج'),
        ('أخرى', 'أخرى'),
    ]
    
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES,
        default='عائلية',
        verbose_name='نوع المناسبة'
    )
    
    guests = models.PositiveIntegerField(
        default=1,
        verbose_name='عدد النزلاء',
        help_text='عدد الأشخاص',
        validators=[MinValueValidator(1)]
    )
    
    # معلومات إضافية
    notes = models.TextField(
        verbose_name='ملاحظات',
        blank=True,
        help_text='أي ملاحظات أو طلبات خاصة'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='حالة الحجز'
    )
    
    # التكلفة
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='السعر الإجمالي',
        null=True,
        blank=True
    )
    
    # التواريخ
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الحجز'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    class Meta:
        verbose_name = 'حجز'
        verbose_name_plural = 'الحجوزات'
        ordering = ['-created_at']
    
    def __str__(self):
        shifts = []
        if self.shift_morning: shifts.append('صباحي')
        if self.shift_evening: shifts.append('مسائي')
        if self.shift_overnight: shifts.append('مبيت')
        shifts_str = " + ".join(shifts) if shifts else "بدون شفت"
        return f"حجز {self.name} - {self.check_in} ({shifts_str})"
    
    def save(self, *args, **kwargs):
        """حساب السعر الإجمالي تلقائياً عند الإنشاء فقط، للسماح للآدمن بتعديله يدوياً أو عند تغير الأسعار العامة"""
        if (not self.pk or self.total_price is None) and self.chalet:
            total = 0
            if self.shift_morning:
                total += self.chalet.morning_price
            if self.shift_evening:
                total += self.chalet.evening_price
            if self.shift_overnight:
                total += self.chalet.overnight_price
            self.total_price = total
        super().save(*args, **kwargs)
    
    def get_shifts_display(self):
        """إرجاع قائمة بأسماء الشفتات المحجوزة"""
        shifts = []
        if self.shift_morning: shifts.append('الصباحي (8 ص - 3 م)')
        if self.shift_evening: shifts.append('المسائي (5 م - 11 م)')
        if self.shift_overnight: shifts.append('المبيت (12 ل - 6 ص)')
        return "، ".join(shifts)
    
    def get_status_display_class(self):
        """إرجاع كلاس CSS حسب حالة الحجز"""
        status_classes = {
            'pending': 'warning',
            'confirmed': 'success',
            'cancelled': 'danger',
            'completed': 'info',
        }
        return status_classes.get(self.status, 'secondary')
    
    @classmethod
    def check_availability(cls, chalet, check_in, shift_morning=False, shift_evening=False, shift_overnight=False, exclude_booking_id=None):
        """
        التحقق من توفر الشاليه في التاريخ والشفتات المحددة
        """
        if not (shift_morning or shift_evening or shift_overnight):
            return False # يجب اختيار شفت واحد على الأقل
            
        # البحث عن الحجوزات في نفس اليوم
        existing_bookings = cls.objects.filter(
            chalet=chalet,
            status='confirmed', # نعتبر الحجوزات المؤكدة فقط محجوزة
            check_in=check_in
        )
        
        # استثناء الحجز الحالي في حالة التعديل
        if exclude_booking_id:
            existing_bookings = existing_bookings.exclude(pk=exclude_booking_id)
        
        for booking in existing_bookings:
            if shift_morning and booking.shift_morning:
                return False
            if shift_evening and booking.shift_evening:
                return False
            if shift_overnight and booking.shift_overnight:
                return False
                    
        return True
    
    @classmethod
    def get_booked_shifts(cls, chalet, date):
        """
        الحصول على الشفتات المحجوزة في يوم معين
        """
        bookings = cls.objects.filter(
            chalet=chalet,
            status='confirmed',
            check_in=date
        )
        
        booked = {
            'morning': False,
            'evening': False,
            'overnight': False
        }
        
        for booking in bookings:
            if booking.shift_morning: booked['morning'] = True
            if booking.shift_evening: booked['evening'] = True
            if booking.shift_overnight: booked['overnight'] = True
            
        return booked


class ContactMessage(models.Model):
    """
    نموذج رسائل الاتصال
    Contact Messages Model
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name='الاسم'
    )
    
    email = models.EmailField(
        verbose_name='البريد الإلكتروني',
        blank=True,
        null=True
    )
    
    phone = models.CharField(
        max_length=15,
        validators=[phone_regex],
        verbose_name='رقم الهاتف'
    )
    
    subject = models.CharField(
        max_length=200,
        verbose_name='الموضوع'
    )
    
    message = models.TextField(
        verbose_name='الرسالة'
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name='تمت القراءة'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإرسال'
    )
    
    class Meta:
        verbose_name = 'رسالة اتصال'
        verbose_name_plural = 'رسائل الاتصال'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"رسالة من {self.name} - {self.subject}"


class Review(models.Model):
    """
    نموذج آراء العملاء
    Customer Reviews Model
    """
    
    chalet = models.ForeignKey(
        Chalet,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='الشاليه'
    )
    
    customer_name = models.CharField(
        max_length=100,
        verbose_name='اسم العميل'
    )
    
    customer_image = models.ImageField(
        upload_to='customer_reviews/',
        verbose_name='صورة العميل',
        blank=True,
        null=True,
        help_text='صورة العميل (اختياري)'
    )
    
    comment = models.TextField(
        verbose_name='التعليق'
    )
    
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1)],
        verbose_name='التقييم',
        help_text='من 1 إلى 5 نجوم'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشط',
        help_text='عرض هذا الرأي في الموقع'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإضافة'
    )
    
    class Meta:
        verbose_name = 'رأي عميل'
        verbose_name_plural = 'آراء العملاء'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"رأي {self.customer_name} - {self.rating} نجوم"


class SiteSettings(models.Model):
    """
    نموذج الإعدادات العامة للموقع (Singleton)
    Global Site Settings Model
    """
    
    # معلومات الموقع الأساسية
    site_name = models.CharField(max_length=100, default='شاليه النرجس', verbose_name='اسم الموقع')
    site_description = models.TextField(default='أفضل شاليه للإيجار اليومي والأسبوعي', verbose_name='وصف الموقع')
    
    # معلومات التواصل
    phone_number = models.CharField(max_length=20, default='+964 778 275 5075', verbose_name='رقم الهاتف الأساسي')
    whatsapp_number = models.CharField(max_length=20, default='+9647782755075', verbose_name='رقم الواتساب', help_text='بدون فواصل، استخدم رمز الدولة مثل +964')
    email_address = models.EmailField(default='info@narjis-chalet.com', verbose_name='البريد الإلكتروني')
    
    # الموقع الجغرافي
    location_text = models.CharField(max_length=200, default='العراق', verbose_name='نص الموقع (العنوان)')
    
    # روابط التواصل الاجتماعي
    facebook_url = models.URLField(blank=True, null=True, verbose_name='رابط فيسبوك')
    instagram_url = models.URLField(blank=True, null=True, verbose_name='رابط انستغرام')
    telegram_url = models.URLField(blank=True, null=True, verbose_name='رابط تيليجرام')
    
    # الألوان
    primary_color = models.CharField(max_length=7, default='#557baf', verbose_name='اللون الأساسي (Primary Color)', help_text='مثال: #557baf')
    primary_dark_color = models.CharField(max_length=7, default='#2862b9', verbose_name='اللون الداكن (Primary Dark)', help_text='مثال: #2862b9')
    primary_light_color = models.CharField(max_length=7, default='#467bbb', verbose_name='اللون الفاتح (Primary Light)', help_text='مثال: #467bbb')
    
    secondary_color = models.CharField(max_length=7, default='#c5a059', verbose_name='اللون الثانوي/الذهبي (Secondary Color)', help_text='مثال: #c5a059')
    secondary_dark_color = models.CharField(max_length=7, default='#a07d3b', verbose_name='اللون الثانوي الداكن (Secondary Dark)', help_text='مثال: #a07d3b')
    secondary_light_color = models.CharField(max_length=7, default='#e5c482', verbose_name='اللون الثانوي الفاتح (Secondary Light)', help_text='مثال: #e5c482')

    class Meta:
        verbose_name = 'إعدادات الموقع'
        verbose_name_plural = 'إعدادات الموقع'
        
    def __str__(self):
        return "إعدادات الموقع العامة"
    
    def save(self, *args, **kwargs):
        """ضمان وجود سجل واحد فقط (Singleton)"""
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """جلب الإعدادات (أو إنشائها إذا لم تكن موجودة)"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class SystemLog(models.Model):
    """
    نموذج سجل عمليات تحركات النظام
    System Activity Log Model
    """
    ACTION_CHOICES = [
        ('create_booking', 'تقديم طلب حجز'),
        ('update_booking_status', 'تحديث حالة حجز'),
        ('delete_booking', 'حذف حجز'),
        ('create_contact_message', 'إرسال رسالة اتصال'),
        ('other', 'عملية أخرى'),
    ]
    
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='المستخدم',
        related_name='system_logs'
    )
    action_type = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        default='other',
        verbose_name='نوع العملية'
    )
    description = models.TextField(
        verbose_name='تفاصيل العملية'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='عنوان IP'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='التاريخ والوقت'
    )

    class Meta:
        verbose_name = 'سجل تحركات النظام'
        verbose_name_plural = 'سجل تحركات النظام'
        ordering = ['-created_at']

    def __str__(self):
        user_str = self.user.username if self.user else "زائر"
        return f"{user_str} - {self.get_action_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


def log_action(user, action_type, description, request=None):
    """
    دالة مساعدة لتسجيل تحركات النظام
    """
    ip = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        if not user and request.user and request.user.is_authenticated:
            user = request.user
            
    SystemLog.objects.create(
        user=user,
        action_type=action_type,
        description=description,
        ip_address=ip
    )
