from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderItem
from cart.models import Cart, CartItem
from accounts.models import Address


@login_required
def checkout(request):
    """صفحه تسویه حساب"""
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or cart.items.count() == 0:
        messages.warning(request, 'سبد خرید شما خالی است')
        return redirect('cart')
    
    addresses = Address.objects.filter(user=request.user)
    
    # محاسبه هزینه ارسال (مثال: 50000 تومان)
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
    """ایجاد سفارش از سبد خرید"""
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
        
        # بررسی موجودی محصولات
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                messages.error(request, f'موجودی محصول {item.product.title} کافی نیست')
                return redirect('cart')
        
        # محاسبه هزینه ارسال بر اساس نوع ارسال
        shipping_type = request.POST.get('send', '4')
        shipping_cost = 19000 if shipping_type == '4' else 32000
        
        # ایجاد سفارش
        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method,
            total_price=cart.get_total_price(),
            shipping_cost=shipping_cost,
            notes=notes,
            status='pending'
        )
        
        # ایجاد آیتم‌های سفارش و کاهش موجودی
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                color=cart_item.color,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # کاهش موجودی
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.sales += cart_item.quantity
            cart_item.product.save()
        
        # خالی کردن سبد خرید
        cart.items.all().delete()
        
        # در حالت واقعی، اینجا باید به درگاه پرداخت متصل شوید
        # برای حالا، پرداخت را به صورت خودکار تایید می‌کنیم
        if payment_method == 'online':
            order.payment_status = True
            order.status = 'paid'
            order.save()
        
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
    """صفحه تکمیل سفارش"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'orders/checkoutComplete.html', {
        'order': order,
        'order_items': order.items.all(),
    })


@login_required
def order_list(request):
    """لیست سفارش‌های کاربر"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })


@login_required
def order_detail(request, order_id):
    """جزئیات یک سفارش"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_items': order.items.all(),
    })
