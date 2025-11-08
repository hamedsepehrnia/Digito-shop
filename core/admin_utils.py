"""
ابزارهای کمکی برای پنل ادمین
"""
from persiantools.jdatetime import JalaliDateTime
from .models import AdminSettings


def format_date_for_admin(datetime_obj, include_time=False):
    """
    تبدیل تاریخ به شمسی یا میلادی بر اساس تنظیمات پنل ادمین
    
    Args:
        datetime_obj: شیء datetime
        include_time: آیا زمان هم نمایش داده شود
    
    Returns:
        رشته تاریخ فرمت شده
    """
    if not datetime_obj:
        return "-"
    
    try:
        settings = AdminSettings.get_settings()
        use_jalali = settings.use_jalali_date
    except:
        use_jalali = True  # پیش‌فرض شمسی
    
    if use_jalali:
        if include_time:
            return JalaliDateTime(datetime_obj).strftime('%Y/%m/%d - %H:%M')
        else:
            return JalaliDateTime(datetime_obj).strftime('%Y/%m/%d')
    else:
        if include_time:
            return datetime_obj.strftime('%Y-%m-%d %H:%M')
        else:
            return datetime_obj.strftime('%Y-%m-%d')

