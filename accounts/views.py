from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import random

from .models import MyUser, PhoneOTP, Address, Favorite
from .forms import CompleteProfileForm, AddressForm
from .utils import send_otp_via_kavenegar, check_otp_rate_limit
from orders.models import Order
from products.models import Product


def user_logout(request):
    logout(request)
    return redirect('/')
@login_required
def dashboard(request):
    """User dashboard main page"""
    from products.models import Product
    from django.db.models import Sum
    
    # Quick statistics
    orders_count = Order.objects.filter(user=request.user).count()
    favorites_count = Favorite.objects.filter(user=request.user).count()
    addresses_count = Address.objects.filter(user=request.user).count()
    
    # Number of delivered orders
    delivered_count = Order.objects.filter(user=request.user, status='delivered').count()
    
    # Account balance (sum of paid orders)
    account_balance = Order.objects.filter(
        user=request.user, 
        payment_status=True
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Points (can be based on purchases)
    points = orders_count * 10  # 10 points per order
    
    # Cancel expired pending orders
    Order.cancel_expired_pending_orders()
    
    # Recent orders
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Recommended products (featured or best-selling products)
    recommended_products = Product.objects.filter(
        stock__gt=0
    ).order_by('-sales', '-created_at')[:8]
    
    # Check favorites for each product
    user_favorites = set(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    context = {
        'orders_count': orders_count,
        'favorites_count': favorites_count,
        'addresses_count': addresses_count,
        'delivered_count': delivered_count,
        'account_balance': account_balance,
        'points': points,
        'recent_orders': recent_orders,
        'recommended_products': recommended_products,
        'user_favorites': user_favorites,
    }
    return render(request, 'accounts/dashboard.html', context)
def dashboard_address(request):
    addresses = Address.objects.filter(user=request.user)
    form = AddressForm()
    return render(request, 'accounts/dashboardAddress.html', {"addresses": addresses, "form": form } )

@require_http_methods(["GET", "POST"])
def add_address_modal(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    form = AddressForm()
    return render(request, 'accounts/dashboardAddress.html', {'form': form})

@require_http_methods(["GET", "POST"])
def edit_address_modal(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    form = AddressForm(instance=address)
    return render(request,'accounts/dashboardAddress.html', {'form': form, "address": address})

def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    return redirect('dashboard-address')

class UserDetailsView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = CompleteProfileForm
    template_name = "accounts/dashboardDetails.html"
    success_url = reverse_lazy("home_page")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.get_object()
        for field, value in form.cleaned_data.items():
            setattr(user, field, value)
        user.save()
        return super().form_valid(form)

@login_required
def dashboard_favorites(request):
    """User favorites page"""
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    products = [fav.product for fav in favorites]
    return render(request, 'accounts/dashboardFavorites.html', {'products': products, 'favorites': favorites})


@require_http_methods(["POST"])
@csrf_exempt
def toggle_favorite(request):
    """Add or remove from favorites"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'error': 'لطفا ابتدا وارد حساب کاربری خود شوید'
        }, status=401)
    
    product_id = request.POST.get('product_id')
    
    try:
        product = Product.objects.get(id=product_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            favorite.delete()
            return JsonResponse({
                'success': True,
                'is_favorite': False,
                'message': 'از علاقه‌مندی‌ها حذف شد'
            })
        else:
            return JsonResponse({
                'success': True,
                'is_favorite': True,
                'message': 'به علاقه‌مندی‌ها اضافه شد'
            })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'محصول یافت نشد'
        }, status=404)


@login_required
def dashboard_orders(request):
    """User orders list"""
    from orders.models import Order
    # Cancel expired pending orders
    Order.cancel_expired_pending_orders()
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/dashboardOrders.html', {'orders': orders})


@login_required
def dashboard_order_details(request, order_id):
    """Order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'accounts/dashboardOrdersDetails.html', {
        'order': order,
        'order_items': order.items.all(),
    })



@csrf_exempt
def send_otp_ajax(request):
    phone = request.POST.get("phone")
    
    if not phone:
        return JsonResponse({"success": False, "error": "شماره تلفن الزامی است"}, status=400)
    
    # Check rate limit
    rate_limit_ok, rate_limit_error = check_otp_rate_limit(phone)
    if not rate_limit_ok:
        return JsonResponse({"success": False, "error": rate_limit_error}, status=429)
    
    # Generate OTP
    otp = f"{random.randint(100000, 999999)}"
    
    # Delete previous OTPs
    PhoneOTP.objects.filter(phone_number=phone).delete()
    
    # Create new OTP
    expiry_minutes = settings.OTP_EXPIRY_MINUTES
    otp_record = PhoneOTP.objects.create(
        phone_number=phone,
        otp=otp,
        expires_at=timezone.now() + timedelta(minutes=expiry_minutes)
    )
    
    # Send OTP
    use_kavenegar = settings.OTP_USE_KAVENEGAR
    is_debug = settings.DEBUG
    
    # If DEBUG=True and OTP_USE_KAVENEGAR=False, return OTP in response
    if is_debug and not use_kavenegar:
        return JsonResponse({"success": True, "otp": otp, "message": "کد تایید در حالت توسعه نمایش داده می‌شود"})
    
    # In production or if OTP_USE_KAVENEGAR=True, use Kavenegar
    if use_kavenegar:
        success, message = send_otp_via_kavenegar(phone, otp)
        if success:
            return JsonResponse({"success": True, "message": "کد تایید به شماره شما ارسال شد"})
        else:
            # Delete OTP if sending fails
            otp_record.delete()
            return JsonResponse({"success": False, "error": message}, status=500)
    
    # If none of the above conditions are met, return OTP in response
    return JsonResponse({"success": True, "otp": otp})


@csrf_exempt
def verify_otp_ajax(request):
    phone = request.POST.get("phone")
    otp = request.POST.get("otp")

    try:
        record = PhoneOTP.objects.get(phone_number=phone, otp=otp)
    except PhoneOTP.DoesNotExist:
        return JsonResponse({"success": False, "error": "invalid"}, status=400)

    if not record.is_valid():
        return JsonResponse({"success": False, "error": "expired"}, status=400)

    user, created = MyUser.objects.get_or_create(phone=phone)
    login(request, user)

    # Sync session cart with user cart
    from cart.views import sync_session_cart_to_user_cart
    sync_session_cart_to_user_cart(request)

    # Redirect based on whether user was just created
    redirect_url = reverse("dashboard-details") if created else reverse("home_page")
    return JsonResponse({"success": True, "redirect": redirect_url})