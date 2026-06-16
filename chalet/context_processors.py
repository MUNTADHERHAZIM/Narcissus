import re
from .models import SiteSettings

def site_settings(request):
    """
    معالج سياق (Context Processor) لتمرير إعدادات الموقع 
    إلى جميع قوالب (Templates) النظام
    """
    try:
        settings = SiteSettings.get_settings()
        if settings:
            if settings.whatsapp_number:
                # تنظيف الرقم من أي فواصل، فراغات (بما فيها الفراغات غير القابلة للكسر) أو رموز
                settings.whatsapp_number_clean = re.sub(r'\D', '', settings.whatsapp_number)
            else:
                settings.whatsapp_number_clean = '9647782755075'

            if settings.phone_number:
                # تنظيف رقم الهاتف مع الحفاظ على علامة + في البداية إن وجدت
                phone = settings.phone_number.strip()
                has_plus = phone.startswith('+')
                digits = re.sub(r'\D', '', phone)
                settings.phone_number_clean = ('+' if has_plus else '') + digits
            else:
                settings.phone_number_clean = '+9647782755075'
        return {'site_settings': settings}
    except Exception:
        # In case the table is not created yet (during migrations)
        return {'site_settings': None}
