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
        fields = ['name', 'email', 'phone', 'check_in', 'check_out', 'guests', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسمك الكامل',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com',
                'required': True,
                'dir': 'ltr',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '07XXXXXXXXX',
                'required': True,
                'dir': 'ltr',
            }),
            'check_in': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'check_out': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50',
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
            'email': 'البريد الإلكتروني',
            'phone': 'رقم الهاتف',
            'check_in': 'تاريخ الوصول',
            'check_out': 'تاريخ المغادرة',
            'guests': 'عدد النزلاء',
            'notes': 'ملاحظات',
        }
        error_messages = {
            'name': {
                'required': 'يرجى إدخال الاسم الكامل',
                'max_length': 'الاسم طويل جداً',
            },
            'email': {
                'required': 'يرجى إدخال البريد الإلكتروني',
                'invalid': 'يرجى إدخال بريد إلكتروني صحيح',
            },
            'phone': {
                'required': 'يرجى إدخال رقم الهاتف',
            },
            'check_in': {
                'required': 'يرجى تحديد تاريخ الوصول',
            },
            'check_out': {
                'required': 'يرجى تحديد تاريخ المغادرة',
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
        today = timezone.now().date().isoformat()
        self.fields['check_in'].widget.attrs['min'] = today
        self.fields['check_out'].widget.attrs['min'] = today
        
        # تعيين الحد الأقصى لعدد النزلاء
        if self.chalet:
            self.fields['guests'].widget.attrs['max'] = self.chalet.max_guests
    
    def clean_check_in(self):
        """التحقق من تاريخ الوصول"""
        check_in = self.cleaned_data.get('check_in')
        
        if check_in:
            today = timezone.now().date()
            if check_in < today:
                raise ValidationError('لا يمكن اختيار تاريخ في الماضي')
        
        return check_in
    
    def clean_check_out(self):
        """التحقق من تاريخ المغادرة"""
        check_out = self.cleaned_data.get('check_out')
        check_in = self.cleaned_data.get('check_in')
        
        if check_out and check_in:
            if check_out <= check_in:
                raise ValidationError('تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول')
        
        return check_out
    
    def clean_guests(self):
        """التحقق من عدد النزلاء"""
        guests = self.cleaned_data.get('guests')
        
        if guests and self.chalet:
            if guests > self.chalet.max_guests:
                raise ValidationError(
                    f'الحد الأقصى لعدد النزلاء هو {self.chalet.max_guests} شخص'
                )
            if guests < 1:
                raise ValidationError('يجب أن يكون عدد النزلاء 1 على الأقل')
        
        return guests
    
    def clean(self):
        """التحقق الشامل من النموذج"""
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        
        # التحقق من توفر التواريخ
        if check_in and check_out and self.chalet:
            is_available = Booking.check_availability(
                self.chalet,
                check_in,
                check_out
            )
            
            if not is_available:
                raise ValidationError(
                    'عذراً، الشاليه محجوز في هذه الفترة. '
                    'يرجى اختيار تواريخ أخرى.'
                )
        
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
                'placeholder': 'example@email.com',
                'required': True,
                'dir': 'ltr',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '07XXXXXXXXX',
                'dir': 'ltr',
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
            'email': 'البريد الإلكتروني',
            'phone': 'رقم الهاتف (اختياري)',
            'subject': 'الموضوع',
            'message': 'الرسالة',
        }
