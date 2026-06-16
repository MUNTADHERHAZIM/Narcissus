"""
نماذج الإدخال لتطبيق الشاليه
Forms for chalet app

النماذج المتوفرة:
- BookingForm: نموذج الحجز
- ContactForm: نموذج الاتصال
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking, ContactMessage


class BookingForm(forms.ModelForm):
    """
    نموذج حجز الشاليه
    Chalet Booking Form
    
    يتضمن التحقق من:
    - صحة التواريخ
    - عدم تداخل الحجوزات
    - عدد النزلاء
    """
    
    class Meta:
        model = Booking
        fields = ['name', 'phone', 'check_in', 'shift_morning', 'shift_evening', 'shift_overnight', 'event_type', 'guests', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسمك الكامل',
                'required': True,
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '07XXXXXXXXX',
                'required': True,
                'dir': 'ltr',
                'pattern': '07[0-9]{9}',
                'maxlength': '11',
                'minlength': '11',
                'title': 'يرجى إدخال رقم هاتف عراقي صحيح مكون من 11 رقماً ويبدأ بـ 07',
            }),
            'check_in': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'required': True,
                'readonly': 'readonly',
                'autocomplete': 'off',
            }),
            'shift_morning': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'shift_evening': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'shift_overnight': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'required': True,
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أي ملاحظات أو طلبات خاصة (اختياري)',
            }),
        }
        labels = {
            'name': 'الاسم الكامل',

            'phone': 'رقم الهاتف',
            'check_in': 'تاريخ الحجز',
            'shift_morning': 'الصباحي (8 ص - 3 م)',
            'shift_evening': 'المسائي (5 م - 11 م)',
            'shift_overnight': 'المبيت (12 ل - 6 ص)',
            'event_type': 'نوع المناسبة',
            'guests': 'عدد النزلاء',
            'notes': 'ملاحظات',
        }
        error_messages = {
            'name': {
                'required': 'يرجى إدخال الاسم الكامل',
                'max_length': 'الاسم طويل جداً',
            },

            'phone': {
                'required': 'يرجى إدخال رقم الهاتف',
            },
            'check_in': {
                'required': 'يرجى تحديد تاريخ الحجز',
            },
            'guests': {
                'required': 'يرجى تحديد عدد النزلاء',
                'min_value': 'يجب أن يكون عدد النزلاء 1 على الأقل',
            },
        }
    
    def __init__(self, *args, chalet=None, **kwargs):
        """تهيئة النموذج مع الشاليه"""
        self.chalet = chalet
        super().__init__(*args, **kwargs)
        
        # تعيين الحد الأدنى لتاريخ الوصول (اليوم)
        today = timezone.localdate().isoformat()
        self.fields['check_in'].widget.attrs['min'] = today
        
        # تم إزالة قيد الحد الأقصى للنزلاء بناء على طلب المستخدم
    
    def clean_check_in(self):
        """التحقق من تاريخ الوصول"""
        check_in = self.cleaned_data.get('check_in')
        
        if check_in:
            today = timezone.localdate()
            if check_in < today:
                raise ValidationError('لا يمكن اختيار تاريخ في الماضي')
        
        return check_in
    
    def clean_guests(self):
        """التحقق من عدد النزلاء"""
        guests = self.cleaned_data.get('guests')
        
        if guests:
            if guests < 1:
                raise ValidationError('يجب أن يكون عدد النزلاء 1 على الأقل')
        
        return guests
        
    def clean(self):
        """التحقق الشامل من النموذج"""
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        shift_morning = cleaned_data.get('shift_morning', False)
        shift_evening = cleaned_data.get('shift_evening', False)
        shift_overnight = cleaned_data.get('shift_overnight', False)
        
        if not (shift_morning or shift_evening or shift_overnight):
            raise ValidationError('لا يتوفر حجز في هذا اليوم او الوقت المختار')
            
        # التحقق من توفر التواريخ والشفتات
        if check_in and self.chalet:
            is_available = Booking.check_availability(
                self.chalet,
                check_in,
                shift_morning=shift_morning,
                shift_evening=shift_evening,
                shift_overnight=shift_overnight
            )
            
            if not is_available:
                raise ValidationError('لا يتوفر حجز في هذا اليوم او الوقت المختار')
        
        return cleaned_data


class ContactForm(forms.ModelForm):
    """
    نموذج الاتصال
    Contact Form
    """
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسمك',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com (اختياري)',
                'dir': 'ltr',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '07XXXXXXXXX',
                'required': True,
                'dir': 'ltr',
                'pattern': '07[0-9]{9}',
                'maxlength': '11',
                'minlength': '11',
                'title': 'يرجى إدخال رقم هاتف عراقي صحيح مكون من 11 رقماً ويبدأ بـ 07',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع الرسالة',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'اكتب رسالتك هنا...',
                'required': True,
            }),
        }
        labels = {
            'name': 'الاسم',
            'email': 'البريد الإلكتروني (اختياري)',
            'phone': 'رقم الهاتف',
            'subject': 'الموضوع',
            'message': 'الرسالة',
        }
