"""
Payment Gateway Integration (Zarinpal)
"""
import requests
import logging
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)


def get_zarinpal_payment_url(amount, description, callback_url, order_id=None):
    """Get payment URL from Zarinpal gateway"""
    merchant_id = settings.ZARINPAL_MERCHANT_ID
    sandbox = settings.ZARINPAL_SANDBOX
    
    logger.info(
        f"ZarinPal Payment Request - Order ID: {order_id}, Amount: {amount}, "
        f"Sandbox: {sandbox}, Description: {description}"
    )
    
    if not merchant_id:
        error_msg = "Merchant ID is not configured"
        logger.error(f"ZarinPal Error: {error_msg}")
        return None, error_msg
    
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
            'order_id': str(order_id)
        } if order_id else {}
    }
    
    try:
        logger.debug(f"ZarinPal Request URL: {url}, Payload: {payload}")
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            logger.debug(f"ZarinPal Response: {result}")
            
            if result.get('data', {}).get('code') == 100:
                authority = result['data']['authority']
                if sandbox:
                    payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"
                else:
                    payment_url = f"https://www.zarinpal.com/pg/StartPay/{authority}"
                
                logger.info(
                    f"ZarinPal Payment URL Created Successfully - Order ID: {order_id}, "
                    f"Authority: {authority}, Payment URL: {payment_url}"
                )
                return payment_url, authority
            else:
                error_code = result.get('data', {}).get('code')
                error_message = result.get('errors', {}).get('message', 'Error creating payment request')
                error_details = result.get('errors', {})
                
                logger.error(
                    f"ZarinPal Payment Request Failed - Order ID: {order_id}, "
                    f"Error Code: {error_code}, Error Message: {error_message}, "
                    f"Full Error Details: {error_details}, Response: {result}"
                )
                return None, error_message
        else:
            error_msg = f"Error connecting to Zarinpal: HTTP {response.status_code}"
            logger.error(
                f"ZarinPal HTTP Error - Order ID: {order_id}, Status Code: {response.status_code}, "
                f"Response Text: {response.text}"
            )
            return None, error_msg
            
    except requests.exceptions.Timeout as e:
        error_msg = f"Timeout connecting to Zarinpal: {str(e)}"
        logger.error(
            f"ZarinPal Timeout Error - Order ID: {order_id}, Error: {str(e)}",
            exc_info=True
        )
        return None, error_msg
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection error to Zarinpal: {str(e)}"
        logger.error(
            f"ZarinPal Connection Error - Order ID: {order_id}, Error: {str(e)}",
            exc_info=True
        )
        return None, error_msg
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to Zarinpal: {str(e)}"
        logger.error(
            f"ZarinPal Request Exception - Order ID: {order_id}, Error: {str(e)}",
            exc_info=True
        )
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.exception(
            f"ZarinPal Unexpected Error - Order ID: {order_id}, Error: {str(e)}"
        )
        return None, error_msg


def verify_zarinpal_payment(authority, amount):
    """Verify Zarinpal payment"""
    merchant_id = settings.ZARINPAL_MERCHANT_ID
    sandbox = settings.ZARINPAL_SANDBOX
    
    logger.info(
        f"ZarinPal Payment Verification - Authority: {authority}, Amount: {amount}, "
        f"Sandbox: {sandbox}"
    )
    
    if not merchant_id:
        error_msg = "Merchant ID is not configured"
        logger.error(f"ZarinPal Verification Error: {error_msg}")
        return False, None, error_msg
    
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
        logger.debug(f"ZarinPal Verify Request URL: {url}, Payload: {payload}")
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            data = result.get('data', {})
            logger.debug(f"ZarinPal Verify Response: {result}")
            
            if data.get('code') == 100:
                # Payment successful
                ref_id = data.get('ref_id')
                logger.info(
                    f"ZarinPal Payment Verified Successfully - Authority: {authority}, "
                    f"Ref ID: {ref_id}, Amount: {amount}"
                )
                return True, ref_id, "Payment completed successfully"
            elif data.get('code') == 101:
                # Payment already verified
                ref_id = data.get('ref_id')
                logger.info(
                    f"ZarinPal Payment Already Verified - Authority: {authority}, "
                    f"Ref ID: {ref_id}, Amount: {amount}"
                )
                return True, ref_id, "Payment already verified"
            else:
                error_code = data.get('code')
                error_message = data.get('message', 'Payment failed')
                logger.error(
                    f"ZarinPal Payment Verification Failed - Authority: {authority}, "
                    f"Error Code: {error_code}, Error Message: {error_message}, "
                    f"Amount: {amount}, Full Response: {result}"
                )
                return False, None, error_message
        else:
            error_msg = f"Error connecting to Zarinpal: HTTP {response.status_code}"
            logger.error(
                f"ZarinPal Verify HTTP Error - Authority: {authority}, "
                f"Status Code: {response.status_code}, Response Text: {response.text}"
            )
            return False, None, error_msg
            
    except requests.exceptions.Timeout as e:
        error_msg = f"Timeout connecting to Zarinpal: {str(e)}"
        logger.error(
            f"ZarinPal Verify Timeout Error - Authority: {authority}, Error: {str(e)}",
            exc_info=True
        )
        return False, None, error_msg
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection error to Zarinpal: {str(e)}"
        logger.error(
            f"ZarinPal Verify Connection Error - Authority: {authority}, Error: {str(e)}",
            exc_info=True
        )
        return False, None, error_msg
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to Zarinpal: {str(e)}"
        logger.error(
            f"ZarinPal Verify Request Exception - Authority: {authority}, Error: {str(e)}",
            exc_info=True
        )
        return False, None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.exception(
            f"ZarinPal Verify Unexpected Error - Authority: {authority}, Error: {str(e)}"
        )
        return False, None, error_msg

