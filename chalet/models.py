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

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='سعر الليلة',
        help_text='السعر بالدينار العراقي',
        validators=[MinValueValidator(0)]
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
        regex=r'^(\+964|0)?7[0-9]{9}$',
        message='أدخل رقم هاتف عراقي صحيح. مثال: 07701234567'
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
    
    # أوقات الحجز
    TIME_CHOICES = [
        ('morning', 'صباحي'),
        ('evening', 'مسائي'),
        ('night', 'ليلي'),
        ('full_day', 'يوم كامل'),
    ]
    
    booking_time = models.CharField(
        max_length=20,
        choices=TIME_CHOICES,
        default='full_day',
        verbose_name='وقت الحجز',
        help_text='اختر وقت الحجز المناسب'
    )
    
    # تفاصيل الحجز
    check_in = models.DateField(
        verbose_name='تاريخ الوصول',
        help_text='تاريخ بداية الإقامة'
    )
    
    check_out = models.DateField(
        verbose_name='تاريخ المغادرة',
        help_text='تاريخ نهاية الإقامة'
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
        return f"حجز {self.name} - {self.check_in} إلى {self.check_out}"
    
    def save(self, *args, **kwargs):
        """حساب السعر الإجمالي تلقائياً"""
        if self.check_in and self.check_out and self.chalet:
            nights = (self.check_out - self.check_in).days
            if nights == 0:
                nights = 1  # لحجوزات نفس اليوم
            if nights > 0:
                self.total_price = nights * self.chalet.price_per_night
        super().save(*args, **kwargs)
    
    def get_nights(self):
        """حساب عدد الليالي"""
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0
    
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
    def check_availability(cls, chalet, check_in, check_out, exclude_booking_id=None, booking_time='full_day'):
        """
        التحقق من توفر الشاليه في التواريخ المحددة
        
        Args:
            chalet: الشاليه المراد التحقق منه
            check_in: تاريخ الوصول
            check_out: تاريخ المغادرة
            exclude_booking_id: معرف الحجز المستثنى (للتعديل)
            booking_time: وقت الحجز
        
        Returns:
            True إذا كان متاحاً، False إذا كان محجوزاً
        """
        # البحث عن حجوزات متداخلة
        overlapping = cls.objects.filter(
            chalet=chalet,
            status='confirmed',
            check_in__lte=check_out,
            check_out__gte=check_in
        )
        
        # استثناء الحجز الحالي في حالة التعديل
        if exclude_booking_id:
            overlapping = overlapping.exclude(pk=exclude_booking_id)
        
        if overlapping.exists():
            for booking in overlapping:
                # إذا كان أحد الحجوزات يوماً كاملاً أو الحجز الجديد يوماً كاملاً، يوجد تعارض
                if booking.booking_time == 'full_day' or booking_time == 'full_day':
                    return False
                # إذا كان نفس الوقت محجوزاً مسبقاً، يوجد تعارض
                if booking.booking_time == booking_time:
                    return False
                    
        return True
    
    @classmethod
    def get_booked_dates(cls, chalet):
        """
        الحصول على التواريخ المحجوزة بالكامل
        """
        booked_dates = []
        bookings = cls.objects.filter(
            chalet=chalet,
            status='confirmed',
            check_out__gte=timezone.now().date()
        )
        
        from collections import defaultdict
        date_times = defaultdict(list)
        
        for booking in bookings:
            current = booking.check_in
            # لحجوزات نفس اليوم يجب أن يتحقق لمرة واحدة على الأقل
            end_date = booking.check_out if booking.check_out > booking.check_in else booking.check_in + timezone.timedelta(days=1)
            while current < end_date:
                date_str = current.strftime('%Y-%m-%d')
                date_times[date_str].append(booking.booking_time)
                current += timezone.timedelta(days=1)
                
        for date_str, times in date_times.items():
            if 'full_day' in times or ('morning' in times and 'evening' in times and 'night' in times):
                booked_dates.append(date_str)
        
        return booked_dates


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
        verbose_name='البريد الإلكتروني'
    )
    
    phone = models.CharField(
        max_length=15,
        verbose_name='رقم الهاتف',
        blank=True
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
    phone_number = models.CharField(max_length=20, default='+964 770 000 0000', verbose_name='رقم الهاتف الأساسي')
    whatsapp_number = models.CharField(max_length=20, default='+9647700000000', verbose_name='رقم الواتساب', help_text='بدون فواصل، استخدم رمز الدولة مثل +964')
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
