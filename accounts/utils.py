"""
Utilities for OTP and SMS sending
"""
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import PhoneOTP


def send_otp_via_kavenegar(phone, otp):
    """Send OTP via Kavenegar SMS service"""
    try:
        api_key = settings.KAVENEGAR_API_KEY
        sender = settings.KAVENEGAR_SENDER
        
        if not api_key:
            return False, "API Key تنظیم نشده است"
        
        url = "https://api.kavenegar.com/v1/{}/sms/send.json".format(api_key)
        payload = {
            'receptor': phone,
            'sender': sender,
            'message': f'کد تایید شما: {otp}\nدیجیتو'
        }
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('return', {}).get('status') == 200:
                return True, "پیامک با موفقیت ارسال شد"
            else:
                return False, result.get('return', {}).get('message', 'خطا در ارسال پیامک')
        else:
            return False, f"خطا در ارتباط با سرور: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return False, f"خطا در ارسال پیامک: {str(e)}"
    except Exception as e:
        return False, f"خطای غیرمنتظره: {str(e)}"


def check_otp_rate_limit(phone):
    """Check OTP request rate limit"""
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)
    
    # Number of requests in the last hour
    requests_last_hour = PhoneOTP.objects.filter(
        phone_number=phone,
        created_at__gte=one_hour_ago
    ).count()
    
    # Number of requests in the last day
    requests_last_day = PhoneOTP.objects.filter(
        phone_number=phone,
        created_at__gte=one_day_ago
    ).count()
    
    max_per_hour = settings.OTP_MAX_REQUESTS_PER_HOUR
    max_per_day = settings.OTP_MAX_REQUESTS_PER_DAY
    
    if requests_last_hour >= max_per_hour:
        return False, f"شما در یک ساعت گذشته {max_per_hour} بار درخواست کد تایید داده‌اید. لطفا کمی صبر کنید."
    
    if requests_last_day >= max_per_day:
        return False, f"شما در یک روز گذشته {max_per_day} بار درخواست کد تایید داده‌اید. لطفا فردا دوباره تلاش کنید."
    
    return True, None

