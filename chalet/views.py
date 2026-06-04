"""
عروض تطبيق الشاليه
Views for chalet app

العروض المتوفرة:
- home: الصفحة الرئيسية
- gallery: معرض الصور
- chalet_detail: تفاصيل الشاليه
- booking: صفحة الحجز
- booking_success: تأكيد الحجز
- contact: صفحة الاتصال
- get_booked_dates: API للتواريخ المحجوزة
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from .models import Chalet, ChaletImage, Booking, Review
from .forms import BookingForm, ContactForm


def home(request):
    """
    الصفحة الرئيسية
    Home Page View
    
    يعرض الشاليه الرئيسي مع صوره ومميزاته
    """
    # جلب الشاليه النشط الأول
    chalet = Chalet.objects.filter(is_active=True).first()
    
    # جلب الصور للسلايدر
    images = []
    features = []
    
    if chalet:
        images = chalet.images.all()[:6]  # أول 6 صور للسلايدر
        features = chalet.features.all()[:8]  # أول 8 مميزات
    
    context = {
        'chalet': chalet,
        'images': images,
        'features': features,
        'page_title': 'الرئيسية',
    }
    
    return render(request, 'chalet/index.html', context)


def gallery(request):
    """
    معرض الصور
    Gallery Page View
    
    يعرض جميع صور الشاليه في شبكة مع Lightbox
    """
    chalet = Chalet.objects.filter(is_active=True).first()
    images = []
    
    if chalet:
        images = chalet.images.all()
    
    context = {
        'chalet': chalet,
        'images': images,
        'page_title': 'معرض الصور',
    }
    
    return render(request, 'chalet/gallery.html', context)


def chalet_detail(request, pk=None):
    """
    تفاصيل الشاليه
    Chalet Detail Page View
    
    يعرض جميع تفاصيل الشاليه ومميزاته وأسعاره
    """
    if pk:
        chalet = get_object_or_404(Chalet, pk=pk, is_active=True)
    else:
        chalet = Chalet.objects.filter(is_active=True).first()
    
    if not chalet:
        messages.warning(request, 'لا يوجد شاليه متاح حالياً')
        return redirect('chalet:home')
    
    # جلب البيانات
    images = chalet.images.all()
    features = chalet.features.all()
    reviews = chalet.reviews.filter(is_active=True)
    
    # الحصول على التواريخ المحجوزة
    booked_dates = Booking.get_booked_dates(chalet)
    
    context = {
        'chalet': chalet,
        'images': images,
        'features': features,
        'reviews': reviews,
        'booked_dates': booked_dates,
        'page_title': f'تفاصيل {chalet.name}',
    }
    
    return render(request, 'chalet/chalet_detail.html', context)


def booking(request, pk=None):
    """
    صفحة الحجز
    Booking Page View
    
    يعرض نموذج الحجز ويعالج طلبات الحجز الجديدة
    """
    # جلب الشاليه
    if pk:
        chalet = get_object_or_404(Chalet, pk=pk, is_active=True)
    else:
        chalet = Chalet.objects.filter(is_active=True).first()
    
    if not chalet:
        messages.warning(request, 'لا يوجد شاليه متاح للحجز حالياً')
        return redirect('chalet:home')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, chalet=chalet)
        
        if form.is_valid():
            # حفظ الحجز
            booking_obj = form.save(commit=False)
            booking_obj.chalet = chalet
            booking_obj.status = 'pending'
            booking_obj.save()
            
            # رسالة نجاح
            messages.success(
                request,
                'تم استلام طلب الحجز بنجاح! سنتواصل معك قريباً للتأكيد.'
            )
            
            return redirect('chalet:booking_success', booking_id=booking_obj.id)
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه')
    else:
        form = BookingForm(chalet=chalet)
    
    # الحصول على التواريخ المحجوزة
    booked_dates = Booking.get_booked_dates(chalet)
    
    context = {
        'chalet': chalet,
        'form': form,
        'booked_dates': booked_dates,
        'page_title': 'حجز الشاليه',
    }
    
    return render(request, 'chalet/booking.html', context)


def booking_success(request, booking_id):
    """
    صفحة تأكيد الحجز
    Booking Success Page View
    
    يعرض تفاصيل الحجز بعد الإرسال الناجح
    """
    booking_obj = get_object_or_404(Booking, id=booking_id)
    
    context = {
        'booking': booking_obj,
        'page_title': 'تم الحجز بنجاح',
    }
    
    return render(request, 'chalet/booking_success.html', context)


def contact(request):
    """
    صفحة الاتصال
    Contact Page View
    
    يعرض نموذج الاتصال ومعلومات التواصل
    """
    chalet = Chalet.objects.filter(is_active=True).first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'تم إرسال رسالتك بنجاح! سنتواصل معك قريباً.'
            )
            return redirect('chalet:contact')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه')
    else:
        form = ContactForm()
    
    context = {
        'chalet': chalet,
        'form': form,
        'page_title': 'اتصل بنا',
    }
    
    return render(request, 'chalet/contact.html', context)


@require_GET
def get_booked_dates(request, pk):
    """
    API للحصول على التواريخ المحجوزة
    API endpoint to get booked dates for a chalet
    
    يُستخدم لتعطيل التواريخ المحجوزة في منتقي التاريخ
    """
    chalet = get_object_or_404(Chalet, pk=pk)
    booked_dates = Booking.get_booked_dates(chalet)
    
    return JsonResponse({
        'booked_dates': booked_dates,
        'chalet_name': chalet.name,
    })


@staff_member_required
def admin_dashboard(request):
    """
    لوحة تحكم الإدارة
    Admin Dashboard View
    """
    bookings = Booking.objects.all().order_by('-created_at')
    
    # إحصائيات
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='pending').count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    
    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'page_title': 'لوحة التحكم | إدارة الحجوزات',
    }
    
    return render(request, 'chalet/dashboard.html', context)


@staff_member_required
def update_booking_status(request, booking_id, status):
    """
    تحديث حالة الحجز
    Update Booking Status View
    """
    booking_obj = get_object_or_404(Booking, id=booking_id)
    
    valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
    if status in valid_statuses:
        booking_obj.status = status
        booking_obj.save()
        messages.success(request, f'تم تحديث حالة الحجز لـ {booking_obj.name} بنجاح.')
    else:
        messages.error(request, 'حالة غير صالحة.')
        
    return redirect('chalet:admin_dashboard')


@staff_member_required
def booking_receipt(request, booking_id):
    """
    فاتورة / وصل الحجز
    Booking Receipt View
    """
    booking_obj = get_object_or_404(Booking, id=booking_id)
    
    # رسالة الواتساب الجاهزة
    import urllib.parse
    status_text = "تم تأكيد حجزك" if booking_obj.status == 'confirmed' else "حالة الحجز: " + booking_obj.get_status_display()
    
    whatsapp_msg = f"""مرحباً {booking_obj.name}،
{status_text} في شاليه النرجس! 🌟

📅 الوصول: {booking_obj.check_in.strftime('%Y/%m/%d')}
📅 المغادرة: {booking_obj.check_out.strftime('%Y/%m/%d')}
💰 المبلغ: {booking_obj.total_price} د.ع

شكراً لاختيارك شاليه النرجس!"""
    
    encoded_msg = urllib.parse.quote(whatsapp_msg)
    whatsapp_link = f"https://wa.me/{booking_obj.phone.replace('+', '')}?text={encoded_msg}"
    
    context = {
        'booking': booking_obj,
        'whatsapp_link': whatsapp_link,
        'page_title': f'وصل حجز #{booking_obj.id}',
    }
    
    return render(request, 'chalet/receipt.html', context)
