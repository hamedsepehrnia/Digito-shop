from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Cart, CartItem
from products.models import Product, Color


def get_session_cart(request):
    """Get cart from session"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def get_cart_total_from_session(request):
    """Calculate total cart items count from session"""
    cart = get_session_cart(request)
    return sum(item.get('quantity', 0) for item in cart.values())


def sync_session_cart_to_user_cart(request):
    """Sync session cart with user cart after login"""
    if not request.user.is_authenticated:
        return
    
    session_cart = get_session_cart(request)
    if not session_cart:
        return
    
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    
    for item_key, item_data in session_cart.items():
        try:
            product_id = item_data.get('product_id')
            color_id = item_data.get('color_id')
            quantity = item_data.get('quantity', 1)
            
            product = Product.objects.get(id=product_id)
            color = None
            if color_id:
                color = Color.objects.get(id=color_id)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart_obj,
                product=product,
                color=color,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock:
                    cart_item.quantity = product.stock
                cart_item.save()
        except (Product.DoesNotExist, Color.DoesNotExist):
            continue
    
    # Clear session cart after sync
    request.session['cart'] = {}


def cart(request):
    """Display cart - for logged-in and guest users"""
    if request.user.is_authenticated:
        cart_obj, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart_obj.items.all()
        total_price = cart_obj.get_total_price()
        
        return render(request, 'cart/cart.html', {
            'cart': cart_obj,
            'cart_items': cart_items,
            'total_price': total_price,
            'is_authenticated': True,
        })
    else:
        # Display cart from session
        session_cart = get_session_cart(request)
        cart_items = []
        total_price = 0
        
        for item_key, item_data in session_cart.items():
            try:
                product = Product.objects.get(id=item_data.get('product_id'))
                color = None
                if item_data.get('color_id'):
                    color = Color.objects.get(id=item_data.get('color_id'))
                
                quantity = item_data.get('quantity', 1)
                item_total = product.price * quantity
                total_price += item_total
                
                cart_items.append({
                    'product': product,
                    'color': color,
                    'quantity': quantity,
                    'item_key': item_key,
                    'get_total_price': lambda: item_total
                })
            except (Product.DoesNotExist, Color.DoesNotExist):
                continue
        
        return render(request, 'cart/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'is_authenticated': False,
        })


@require_http_methods(["POST"])
@csrf_exempt
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    color_id = request.POST.get('color_id', None)
    quantity = int(request.POST.get('quantity', 1))

    try:
        product = Product.objects.get(id=product_id)
        
        # Check stock
        if product.stock < quantity:
            return JsonResponse({
                'success': False,
                'error': 'موجودی کافی نیست'
            }, status=400)

        # If user is logged in
        if request.user.is_authenticated:
            cart_obj, created = Cart.objects.get_or_create(user=request.user)
            
            color = None
            if color_id:
                color = Color.objects.get(id=color_id)

            # Add or update item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart_obj,
                product=product,
                color=color,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock:
                    cart_item.quantity = product.stock
                cart_item.save()

            cart_total = cart_obj.get_total_items()
        else:
            # Use session for guest users
            session_cart = get_session_cart(request)
            
            # Create unique key for item
            item_key = f"{product_id}_{color_id or 'none'}"
            
            if item_key in session_cart:
                # Update quantity
                session_cart[item_key]['quantity'] += quantity
                if session_cart[item_key]['quantity'] > product.stock:
                    session_cart[item_key]['quantity'] = product.stock
            else:
                # Add new item
                session_cart[item_key] = {
                    'product_id': product_id,
                    'color_id': color_id,
                    'quantity': quantity
                }
            
            request.session['cart'] = session_cart
            request.session.modified = True
            cart_total = get_cart_total_from_session(request)

        return JsonResponse({
            'success': True,
            'message': 'محصول به سبد خرید اضافه شد',
            'cart_total': cart_total
        })

    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'محصول یافت نشد'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_cart_item(request, item_id):
    quantity = int(request.POST.get('quantity', 1))

    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'آیتم حذف شد'
            })

        if quantity > cart_item.product.stock:
            return JsonResponse({
                'success': False,
                'error': 'موجودی کافی نیست'
            }, status=400)

        cart_item.quantity = quantity
        cart_item.save()

        cart_obj = cart_item.cart
        return JsonResponse({
            'success': True,
            'item_total': cart_item.get_total_price(),
            'cart_total': cart_obj.get_total_price(),
            'cart_items_count': cart_obj.get_total_items()
        })

    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'آیتم یافت نشد'
        }, status=404)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_obj = cart_item.cart
        cart_item.delete()

        return JsonResponse({
            'success': True,
            'message': 'آیتم حذف شد',
            'cart_total': cart_obj.get_total_price(),
            'cart_items_count': cart_obj.get_total_items()
        })

    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'آیتم یافت نشد'
        }, status=404)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def clear_cart(request):
    try:
        cart_obj = Cart.objects.get(user=request.user)
        cart_obj.items.all().delete()
        return JsonResponse({
            'success': True,
            'message': 'سبد خرید خالی شد'
        })
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'سبد خرید یافت نشد'
        }, status=404)


@require_http_methods(["POST"])
@csrf_exempt
def update_session_cart_item(request, item_key):
    """Update item quantity in session cart"""
    quantity = int(request.POST.get('quantity', 1))
    
    session_cart = get_session_cart(request)
    
    if item_key not in session_cart:
        return JsonResponse({
            'success': False,
            'error': 'آیتم یافت نشد'
        }, status=404)
    
    try:
        product = Product.objects.get(id=session_cart[item_key].get('product_id'))
        
        if quantity <= 0:
            del session_cart[item_key]
            request.session.modified = True
            return JsonResponse({
                'success': True,
                'message': 'آیتم حذف شد',
                'cart_total': 0,
                'cart_items_count': get_cart_total_from_session(request)
            })
        
        if quantity > product.stock:
            return JsonResponse({
                'success': False,
                'error': 'موجودی کافی نیست'
            }, status=400)
        
        session_cart[item_key]['quantity'] = quantity
        request.session.modified = True
        
        # Calculate total price
        total_price = 0
        for item_data in session_cart.values():
            try:
                prod = Product.objects.get(id=item_data.get('product_id'))
                qty = item_data.get('quantity', 1)
                total_price += prod.price * qty
            except Product.DoesNotExist:
                continue
        
        # Calculate item price
        item_total = product.price * quantity
        
        return JsonResponse({
            'success': True,
            'item_total': item_total,
            'cart_total': total_price,
            'cart_items_count': get_cart_total_from_session(request)
        })
    
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'محصول یافت نشد'
        }, status=404)


@require_http_methods(["POST"])
@csrf_exempt
def remove_session_cart_item(request, item_key):
    """Remove item from session cart"""
    session_cart = get_session_cart(request)
    
    if item_key not in session_cart:
        return JsonResponse({
            'success': False,
            'error': 'آیتم یافت نشد'
        }, status=404)
    
    del session_cart[item_key]
    request.session.modified = True
    
    # Calculate total price
    total_price = 0
    for item_data in session_cart.values():
        try:
            product = Product.objects.get(id=item_data.get('product_id'))
            quantity = item_data.get('quantity', 1)
            total_price += product.price * quantity
        except Product.DoesNotExist:
            continue
    
    return JsonResponse({
        'success': True,
        'message': 'آیتم حذف شد',
        'cart_total': total_price,
        'cart_items_count': get_cart_total_from_session(request)
    })
