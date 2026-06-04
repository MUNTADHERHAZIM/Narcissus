from .models import SiteSettings

def site_settings(request):
    """
    معالج سياق (Context Processor) لتمرير إعدادات الموقع 
    إلى جميع قوالب (Templates) النظام
    """
    try:
        settings = SiteSettings.get_settings()
        return {'site_settings': settings}
    except Exception:
        # In case the table is not created yet (during migrations)
        return {'site_settings': None}
