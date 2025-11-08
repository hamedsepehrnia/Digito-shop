"""
Payment Gateway Integration (Zarinpal)
"""
import requests
from django.conf import settings
from django.urls import reverse


def get_zarinpal_payment_url(amount, description, callback_url, order_id=None):
    """Get payment URL from Zarinpal gateway"""
    merchant_id = settings.ZARINPAL_MERCHANT_ID
    sandbox = settings.ZARINPAL_SANDBOX
    
    if not merchant_id:
        return None, "Merchant ID is not configured"
    
    # URL based on sandbox or production
    if sandbox:
        url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    else:
        url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    
    payload = {
        'merchant_id': merchant_id,
        'amount': amount,  # Amount in Rials
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
                return None, result.get('errors', {}).get('message', 'Error creating payment request')
        else:
            return None, f"Error connecting to Zarinpal: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return None, f"Error connecting to Zarinpal: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def verify_zarinpal_payment(authority, amount):
    """Verify Zarinpal payment"""
    merchant_id = settings.ZARINPAL_MERCHANT_ID
    sandbox = settings.ZARINPAL_SANDBOX
    
    if not merchant_id:
        return False, None, "Merchant ID is not configured"
    
    # URL based on sandbox or production
    if sandbox:
        url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    else:
        url = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    
    payload = {
        'merchant_id': merchant_id,
        'amount': amount,  # Amount in Rials
        'authority': authority
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            data = result.get('data', {})
            
            if data.get('code') == 100:
                # Payment successful
                ref_id = data.get('ref_id')
                return True, ref_id, "Payment completed successfully"
            elif data.get('code') == 101:
                # Payment already verified
                ref_id = data.get('ref_id')
                return True, ref_id, "Payment already verified"
            else:
                return False, None, data.get('message', 'Payment failed')
        else:
            return False, None, f"Error connecting to Zarinpal: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return False, None, f"Error connecting to Zarinpal: {str(e)}"
    except Exception as e:
        return False, None, f"Unexpected error: {str(e)}"

