import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse

from .models import Order, OrderItem
from .payment import get_zarinpal_payment_url, verify_zarinpal_payment
from cart.models import Cart, CartItem
from accounts.models import Address

logger = logging.getLogger(__name__)


@login_required
def checkout(request):
    """Checkout page"""
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or cart.items.count() == 0:
        messages.warning(request, 'سبد خرید شما خالی است')
        return redirect('cart')
    
    addresses = Address.objects.filter(user=request.user)
    
    # Calculate shipping cost (example: 50000 Rials)
    shipping_cost = 50000
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'addresses': addresses,
        'shipping_cost': shipping_cost,
        'total_price': cart.get_total_price(),
        'final_price': cart.get_total_price() + shipping_cost,
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
@require_http_methods(["POST"])
def create_order(request):
    """Create order from cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        
        if cart.items.count() == 0:
            messages.warning(request, 'سبد خرید شما خالی است')
            return redirect('cart')
        
        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment_method', 'online')
        notes = request.POST.get('notes', '')
        
        if not address_id:
            messages.error(request, 'لطفا آدرس را انتخاب کنید')
            return redirect('checkout')
        
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, 'آدرس یافت نشد')
            return redirect('checkout')
        
        # Check product stock
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                messages.error(request, f'موجودی محصول {item.product.title} کافی نیست')
                return redirect('cart')
        
        # Calculate shipping cost based on shipping type
        shipping_type = request.POST.get('send', '4')
        shipping_cost = 19000 if shipping_type == '4' else 32000
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method,
            total_price=cart.get_total_price(),
            shipping_cost=shipping_cost,
            notes=notes,
            status='pending'
        )
        
        # Create order items and reduce stock
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                color=cart_item.color,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Reduce stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.sales += cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        # Process payment
        if payment_method == 'online':
            # Check if Zarinpal is active
            if settings.ZARINPAL_ACTIVE:
                # Use Zarinpal payment gateway
                final_price = order.get_final_price()
                description = f"پرداخت سفارش {order.order_number}"
                callback_url = request.build_absolute_uri(reverse('zarinpal_callback'))
                
                payment_url, authority = get_zarinpal_payment_url(
                    amount=final_price,
                    description=description,
                    callback_url=callback_url,
                    order_id=order.id
                )
                
                logger.info(
                    f"ZarinPal Payment URL Result - Order ID: {order.id}, "
                    f"Payment URL: {payment_url}, Authority: {authority}, "
                    f"Payment URL Type: {type(payment_url)}, Payment URL Bool: {bool(payment_url)}"
                )
                
                if payment_url and payment_url.strip():
                    # Store authority in session for use in callback
                    request.session['zarinpal_authority'] = authority
                    request.session['zarinpal_order_id'] = order.id
                    request.session.modified = True  # Ensure session is saved
                    logger.info(
                        f"Redirecting to ZarinPal payment - Order ID: {order.id}, "
                        f"User: {request.user.phone}, Authority: {authority}, "
                        f"Payment URL: {payment_url}"
                    )
                    return redirect(payment_url)
                else:
                    error_message = f'خطا در اتصال به درگاه پرداخت: {authority}'
                    logger.error(
                        f"ZarinPal Payment URL Creation Failed in View - Order ID: {order.id}, "
                        f"User: {request.user.phone}, Error: {authority}, Amount: {final_price}"
                    )
                    messages.error(request, error_message)
                    return redirect('checkout')
            else:
                # Auto payment (for testing)
                order.payment_status = True
                order.status = 'paid'
                order.save()
                messages.success(request, 'سفارش شما با موفقیت ثبت و پرداخت شد')
                return redirect('checkout_complete', order_id=order.id)
        else:
            # Cash on delivery payment
            messages.success(request, 'سفارش شما با موفقیت ثبت شد')
            return redirect('checkout_complete', order_id=order.id)
        
    except Cart.DoesNotExist:
        messages.error(request, 'سبد خرید یافت نشد')
        return redirect('cart')
    except Exception as e:
        messages.error(request, f'خطا در ثبت سفارش: {str(e)}')
        return redirect('checkout')


@login_required
def checkout_complete(request, order_id):
    """Order completion page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'orders/checkoutComplete.html', {
        'order': order,
        'order_items': order.items.all(),
    })


@login_required
def order_list(request):
    """User orders list"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })


@login_required
def order_detail(request, order_id):
    """Order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_items': order.items.all(),
    })


@login_required
def zarinpal_callback(request):
    """Zarinpal payment callback after payment"""
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    
    logger.info(
        f"ZarinPal Callback Received - Authority: {authority}, Status: {status}, "
        f"User: {request.user.phone}, GET Params: {dict(request.GET)}"
    )
    
    # Get data from session
    session_authority = request.session.get('zarinpal_authority')
    order_id = request.session.get('zarinpal_order_id')
    
    if not order_id:
        logger.error(
            f"ZarinPal Callback Error: Order ID not found in session - "
            f"User: {request.user.phone}, Authority: {authority}, Status: {status}"
        )
        messages.error(request, 'سفارش یافت نشد')
        return redirect('checkout')
    
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    except Exception as e:
        logger.error(
            f"ZarinPal Callback Error: Order not found - Order ID: {order_id}, "
            f"User: {request.user.phone}, Error: {str(e)}",
            exc_info=True
        )
        messages.error(request, 'سفارش یافت نشد')
        return redirect('checkout')
    
    # Clear session
    if 'zarinpal_authority' in request.session:
        del request.session['zarinpal_authority']
    if 'zarinpal_order_id' in request.session:
        del request.session['zarinpal_order_id']
    
    if status == 'OK' and authority == session_authority:
        # Verify payment
        final_price = order.get_final_price()
        logger.info(
            f"ZarinPal Callback Verification Started - Order ID: {order.id}, "
            f"Authority: {authority}, Amount: {final_price}, User: {request.user.phone}"
        )
        
        success, ref_id, message = verify_zarinpal_payment(authority, final_price)
        
        if success:
            order.payment_status = True
            order.status = 'paid'
            # You can store ref_id in a field if needed
            order.save()
            logger.info(
                f"ZarinPal Payment Completed Successfully - Order ID: {order.id}, "
                f"Ref ID: {ref_id}, Authority: {authority}, User: {request.user.phone}"
            )
            messages.success(request, f'پرداخت با موفقیت انجام شد. کد پیگیری: {ref_id}')
            return redirect('checkout_complete', order_id=order.id)
        else:
            logger.error(
                f"ZarinPal Payment Verification Failed in Callback - Order ID: {order.id}, "
                f"Authority: {authority}, Error Message: {message}, "
                f"Amount: {final_price}, User: {request.user.phone}"
            )
            messages.error(request, f'خطا در تایید پرداخت: {message}')
            return redirect('checkout')
    else:
        logger.warning(
            f"ZarinPal Payment Cancelled or Invalid - Order ID: {order.id}, "
            f"Status: {status}, Authority: {authority}, "
            f"Session Authority: {session_authority}, User: {request.user.phone}"
        )
        messages.warning(request, 'پرداخت لغو شد')
        return redirect('checkout')


@login_required
def retry_payment(request, order_id):
    """Retry payment for a pending order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is eligible for payment
    if order.status != 'pending' or order.payment_status:
        messages.error(request, 'این سفارش قابل پرداخت نیست')
        return redirect('dashboard-orders')
    
    # Check if order is expired
    if order.is_pending_payment_expired():
        order.status = 'cancelled'
        order.save()
        messages.error(request, 'زمان پرداخت این سفارش به پایان رسیده است')
        return redirect('dashboard-orders')
    
    # Check if Zarinpal is active
    if not settings.ZARINPAL_ACTIVE:
        messages.error(request, 'درگاه پرداخت فعال نیست')
        return redirect('dashboard-orders')
    
    # Create payment URL
    final_price = order.get_final_price()
    description = f"پرداخت سفارش {order.order_number}"
    callback_url = request.build_absolute_uri(reverse('zarinpal_callback'))
    
    payment_url, authority = get_zarinpal_payment_url(
        amount=final_price,
        description=description,
        callback_url=callback_url,
        order_id=order.id
    )
    
    if payment_url:
        # Store authority in session for use in callback
        request.session['zarinpal_authority'] = authority
        request.session['zarinpal_order_id'] = order.id
        request.session.modified = True
        logger.info(
            f"Retry Payment - Redirecting to ZarinPal - Order ID: {order.id}, "
            f"User: {request.user.phone}, Authority: {authority}"
        )
        return redirect(payment_url)
    else:
        logger.error(
            f"Retry Payment Failed - Order ID: {order.id}, "
            f"User: {request.user.phone}, Error: {authority}"
        )
        messages.error(request, f'خطا در اتصال به درگاه پرداخت: {authority}')
        return redirect('dashboard-orders')
