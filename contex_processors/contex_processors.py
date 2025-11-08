from cart.models import Cart


def get_session_cart(request):
    """دریافت سبد خرید از session"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def cart_context(request):
    """Context processor برای نمایش اطلاعات سبد خرید در تمام صفحات"""
    context = {
        'cart_items_count': 0,
        'cart_total_price': 0,
        'cart': None,
    }
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.prefetch_related('items__product__images').get(user=request.user)
            context['cart'] = cart
            context['cart_items_count'] = cart.get_total_items()
            context['cart_total_price'] = cart.get_total_price()
        except Cart.DoesNotExist:
            pass
    else:
        # محاسبه از session برای کاربران غیرلاگین
        session_cart = get_session_cart(request)
        context['cart_items_count'] = sum(item.get('quantity', 0) for item in session_cart.values())
        
        # محاسبه قیمت کل
        from products.models import Product
        total_price = 0
        for item_data in session_cart.values():
            try:
                product = Product.objects.get(id=item_data.get('product_id'))
                quantity = item_data.get('quantity', 1)
                total_price += product.price * quantity
            except Product.DoesNotExist:
                continue
        context['cart_total_price'] = total_price
    
    return context


def categories_context(request):
    """Context processor برای نمایش دسته‌بندی‌ها در ناوبری با ساختار درختی MPTT"""
    try:
        from products.models import Category
        # فقط سطح ریشه، ولی همه‌ی زیرشاخه‌ها را Prefetch کن تا در Template سریع‌تر رندر شود
        categories = (
            Category.objects.filter(parent__isnull=True)
            .exclude(slug='')
            .prefetch_related(
                'children__children__children'  # تا سه سطح
            )
            .order_by('name')
        )
        return {'categories': categories}
    except Exception as e:
        # بهتره خطا لاگ بشه تا راحت‌تر پیدا کنی کجاست
        import logging
        logging.error(f"Category context error: {e}")
        return {'categories': []}



def contact_info_context(request):
    """Context processor برای نمایش اطلاعات تماس در هدر و فوتر"""
    try:
        from core.models import ContactInfo
        contact_info = ContactInfo.objects.filter(is_active=True).first()
        return {'contact_info': contact_info}
    except Exception:
        return {'contact_info': None}


def footer_context(request):
    """Context processor برای نمایش اطلاعات فوتر"""
    try:
        from core.models import FooterLinkGroup, SocialMedia, FooterSettings
        footer_groups = FooterLinkGroup.objects.filter(is_active=True).prefetch_related('links').order_by('order')
        social_media = SocialMedia.objects.filter(is_active=True).order_by('order')
        footer_settings = FooterSettings.objects.filter(is_active=True).first()
        
        return {
            'footer_groups': footer_groups,
            'social_media': social_media,
            'footer_settings': footer_settings,
        }
    except Exception:
        return {
            'footer_groups': [],
            'social_media': [],
            'footer_settings': None,
        }

