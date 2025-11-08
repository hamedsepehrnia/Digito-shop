"""
Payment Gateway Integration (Zarinpal)
"""
import requests
from django.conf import settings
from django.urls import reverse


def get_zarinpal_payment_url(amount, description, callback_url, order_id=None):
    """دریافت لینک پرداخت از زرین‌پال"""
    merchant_id = settings.ZARINPAL_MERCHANT_ID
    sandbox = settings.ZARINPAL_SANDBOX
    
    if not merchant_id:
        return None, "Merchant ID تنظیم نشده است"
    
    # URL بر اساس sandbox یا production
    if sandbox:
        url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    else:
        url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    
    payload = {
        'merchant_id': merchant_id,
        'amount': amount,  # به ریال
        'description': description,
        'callback_url': callback_url,
        'metadata': {
            'order_id': order_id
        } if order_id else {}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('data', {}).get('code') == 100:
                authority = result['data']['authority']
                if sandbox:
                    payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"
                else:
                    payment_url = f"https://www.zarinpal.com/pg/StartPay/{authority}"
                return payment_url, authority
            else:
                return None, result.get('errors', {}).get('message', 'خطا در ایجاد درخواست پرداخت')
        else:
            return None, f"خطا در ارتباط با زرین‌پال: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return None, f"خطا در ارتباط با زرین‌پال: {str(e)}"
    except Exception as e:
        return None, f"خطای غیرمنتظره: {str(e)}"


def verify_zarinpal_payment(authority, amount):
    """تایید پرداخت زرین‌پال"""
    merchant_id = settings.ZARINPAL_MERCHANT_ID
    sandbox = settings.ZARINPAL_SANDBOX
    
    if not merchant_id:
        return False, None, "Merchant ID تنظیم نشده است"
    
    # URL بر اساس sandbox یا production
    if sandbox:
        url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    else:
        url = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    
    payload = {
        'merchant_id': merchant_id,
        'amount': amount,  # به ریال
        'authority': authority
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            data = result.get('data', {})
            
            if data.get('code') == 100:
                # پرداخت موفق
                ref_id = data.get('ref_id')
                return True, ref_id, "پرداخت با موفقیت انجام شد"
            elif data.get('code') == 101:
                # پرداخت قبلا تایید شده
                ref_id = data.get('ref_id')
                return True, ref_id, "پرداخت قبلا تایید شده است"
            else:
                return False, None, data.get('message', 'پرداخت ناموفق بود')
        else:
            return False, None, f"خطا در ارتباط با زرین‌پال: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return False, None, f"خطا در ارتباط با زرین‌پال: {str(e)}"
    except Exception as e:
        return False, None, f"خطای غیرمنتظره: {str(e)}"

