/**
 * ملف JavaScript الرئيسي لموقع شاليه النرجس
 * Main JavaScript file for Narjis Chalet website
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // =============================================
    // 1. شريط التنقل - Navbar Scroll Effect
    // =============================================
    
    const navbar = document.querySelector('.navbar');
    
    function handleNavbarScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    
    window.addEventListener('scroll', handleNavbarScroll);
    handleNavbarScroll(); // Check on load
    
    // =============================================
    // 2. زر العودة للأعلى - Back to Top Button
    // =============================================
    
    const backToTop = document.getElementById('backToTop');
    
    function handleBackToTop() {
        if (window.scrollY > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    }
    
    window.addEventListener('scroll', handleBackToTop);
    
    if (backToTop) {
        backToTop.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // =============================================
    // 3. إغلاق الرسائل التلقائي - Auto-dismiss Alerts
    // =============================================
    
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // إغلاق بعد 5 ثواني
    });
    
    // =============================================
    // 4. التحقق من النماذج - Form Validation
    // =============================================
    
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // =============================================
    // 5. تنسيق أرقام الهاتف - Phone Number Formatting
    // =============================================
    
    const phoneInputs = document.querySelectorAll('input[type="tel"], input#id_phone');
    
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            // إزالة أي حروف غير رقمية
            let value = e.target.value.replace(/\D/g, '');
            
            // تحديد الطول الأقصى
            if (value.length > 11) {
                value = value.slice(0, 11);
            }
            
            e.target.value = value;
        });
    });
    
    // =============================================
    // 6. تأثيرات التمرير - Scroll Animations
    // =============================================
    
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .gallery-card, .detail-card');
        
        elements.forEach(function(element) {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // إضافة الأنماط الأولية
    document.querySelectorAll('.feature-card, .gallery-card, .detail-card').forEach(function(element) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.5s ease';
    });
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // تشغيل عند التحميل
    
    // =============================================
    // 7. التحقق من تداخل التواريخ - Date Overlap Check
    // =============================================
    
    const checkInInput = document.getElementById('id_check_in');
    const checkOutInput = document.getElementById('id_check_out');
    
    if (checkInInput && checkOutInput) {
        checkInInput.addEventListener('change', function() {
            // تحديث الحد الأدنى لتاريخ المغادرة
            if (this.value) {
                const checkInDate = new Date(this.value);
                const minCheckOut = new Date(checkInDate);
                minCheckOut.setDate(minCheckOut.getDate() + 1);
                
                checkOutInput.min = minCheckOut.toISOString().split('T')[0];
                
                // إذا كان تاريخ المغادرة أقل من تاريخ الوصول، إفراغه
                if (checkOutInput.value && new Date(checkOutInput.value) <= checkInDate) {
                    checkOutInput.value = '';
                }
            }
        });
        
        checkOutInput.addEventListener('change', function() {
            if (checkInInput.value && this.value) {
                const checkIn = new Date(checkInInput.value);
                const checkOut = new Date(this.value);
                
                if (checkOut <= checkIn) {
                    alert('تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول');
                    this.value = '';
                }
            }
        });
    }
    
    // =============================================
    // 8. معاينة عدد الليالي - Nights Preview
    // =============================================
    
    function updateNightsPreview() {
        const checkIn = document.getElementById('id_check_in');
        const checkOut = document.getElementById('id_check_out');
        const nightsDisplay = document.getElementById('nightsCount');
        const totalDisplay = document.getElementById('totalPrice');
        const calculator = document.getElementById('priceCalculator');
        
        if (checkIn && checkOut && checkIn.value && checkOut.value) {
            const date1 = new Date(checkIn.value);
            const date2 = new Date(checkOut.value);
            const diffTime = Math.abs(date2 - date1);
            const nights = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            if (nightsDisplay) {
                nightsDisplay.textContent = nights;
            }
            
            if (calculator) {
                calculator.style.display = 'block';
            }
        }
    }
    
    if (checkInInput) {
        checkInInput.addEventListener('change', updateNightsPreview);
    }
    
    if (checkOutInput) {
        checkOutInput.addEventListener('change', updateNightsPreview);
    }
    
    // =============================================
    // 9. تحميل الصور الكسول - Lazy Loading Images
    // =============================================
    
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // =============================================
    // 10. تفعيل Tooltips
    // =============================================
    
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // =============================================
    // 11. نسخ رقم الحجز - Copy Booking ID
    // =============================================
    
    const bookingIdElement = document.querySelector('.booking-id');
    
    if (bookingIdElement) {
        bookingIdElement.style.cursor = 'pointer';
        bookingIdElement.title = 'انقر للنسخ';
        
        bookingIdElement.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(function() {
                const originalText = bookingIdElement.textContent;
                bookingIdElement.textContent = 'تم النسخ!';
                setTimeout(function() {
                    bookingIdElement.textContent = originalText;
                }, 1500);
            });
        });
    }
    
    // =============================================
    // 12. عداد الأحرف في الملاحظات - Character Counter
    // =============================================
    
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(function(textarea) {
        const maxLength = textarea.getAttribute('maxlength');
        
        if (maxLength) {
            const counter = document.createElement('small');
            counter.className = 'text-muted d-block text-end mt-1';
            counter.textContent = `0 / ${maxLength}`;
            
            textarea.parentNode.appendChild(counter);
            
            textarea.addEventListener('input', function() {
                counter.textContent = `${this.value.length} / ${maxLength}`;
            });
        }
    });
    
    // =============================================
    // 13. تأكيد الإرسال - Form Submit Confirmation
    // =============================================
    
    const bookingForm = document.getElementById('bookingForm');
    
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> جاري الإرسال...';
            }
        });
    }
    
    // =============================================
    // 14. التمرير السلس للروابط - Smooth Scroll for Anchors
    // =============================================
    
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            if (targetId !== '#') {
                e.preventDefault();
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    const navbarHeight = navbar ? navbar.offsetHeight : 0;
                    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    console.log('🏡 شاليه النرجس - تم تحميل الموقع بنجاح');
});
