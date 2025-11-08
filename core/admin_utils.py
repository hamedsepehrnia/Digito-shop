"""
Admin panel utility functions
"""
from persiantools.jdatetime import JalaliDateTime
from .models import AdminSettings


def format_date_for_admin(datetime_obj, include_time=False):
    """
    Convert date to Jalali or Gregorian based on admin panel settings
    
    Args:
        datetime_obj: datetime object
        include_time: whether to include time in display
    
    Returns:
        formatted date string
    """
    if not datetime_obj:
        return "-"
    
    try:
        settings = AdminSettings.get_settings()
        use_jalali = settings.use_jalali_date
    except:
        use_jalali = True  # Default to Jalali
    
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

