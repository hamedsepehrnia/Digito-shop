from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Min, Max
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Color, Category, Comment, Brand
from .forms import CommentForm
from accounts.models import Favorite


def shop(request):
    """صفحه فروشگاه با فیلتر و جستجو"""
    products = Product.objects.all()
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # فیلتر بر اساس برند
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    
    # فیلتر بر اساس رنگ
    color_id = request.GET.get('color')
    if color_id:
        products = products.filter(colors__id=color_id)
    
    # فیلتر بر اساس قیمت
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except ValueError:
            pass
    
    # فیلتر محصولات شگفت‌انگیز
    is_amazing = request.GET.get('is_amazing')
    if is_amazing == 'true':
        products = products.filter(is_amazing=True)
    
    # فیلتر فقط کالاهای موجود
    only_available = request.GET.get('only_available')
    if only_available == 'true':
        products = products.filter(stock__gt=0)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(english_title__icontains=search_query)
        )
    
    # مرتب‌سازی
    sort_by = request.GET.get('sort', 'created_at')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'sales':
        products = products.order_by('-sales')
    elif sort_by == 'views':
        products = products.order_by('-views')
    else:
        products = products.order_by('-created_at')
    
    # محاسبه محدوده قیمت برای فیلتر
    price_range = products.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )
    
    # صفحه‌بندی
    paginator = Paginator(products, 12)  # 12 محصول در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # دریافت دسته‌بندی‌های مناسب برای فیلتر (نه برای منوی اصلی)
    # اگر دسته‌بندی انتخاب شده، فرزندان آن را نمایش می‌دهیم
    # در غیر این صورت، دسته‌بندی‌های ریشه را نمایش می‌دهیم
    selected_category_obj = None
    if category_slug:
        try:
            selected_category_obj = Category.objects.get(slug=category_slug)
            # نمایش فرزندان دسته‌بندی انتخاب شده
            filter_categories = selected_category_obj.get_children().order_by('name')
        except Category.DoesNotExist:
            filter_categories = Category.objects.filter(parent__isnull=True).exclude(slug='').order_by('name')
    else:
        # نمایش دسته‌بندی‌های ریشه
        filter_categories = Category.objects.filter(parent__isnull=True).exclude(slug='').order_by('name')
    colors = Color.objects.distinct()
    brands = Brand.objects.filter(is_active=True).order_by('order', 'name')
    
    # بررسی favorite برای کاربران لاگین شده
    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    context = {
        'products': page_obj,
        'filter_categories': filter_categories,  # فقط برای فیلتر سمت راست
        'selected_category_obj': selected_category_obj,  # برای نمایش مسیر دسته‌بندی
        'colors': colors,
        'brands': brands,
        'selected_category': category_slug,
        'selected_brand': brand_slug,
        'selected_color': color_id,
        'search_query': search_query,
        'price_range': price_range,
        'sort_by': sort_by,
        'user_favorites': user_favorites,
        'only_available': only_available == 'true',
    }
    
    return render(request, 'products/shop.html', context)


def single_product(request, slug):
    """صفحه جزئیات محصول"""
    product = get_object_or_404(Product, slug=slug)
    
    # افزایش تعداد بازدید
    product.views += 1
    product.save(update_fields=['views'])
    
    # محصولات مرتبط (از همان دسته‌بندی)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk)[:4]
    
    # نظرات تایید شده
    comments = product.comments.all().order_by('-created_at')
    
    # فرم نظر
    comment_form = CommentForm()
    
    # بررسی علاقه‌مندی
    is_favorite = False
    user_favorites = set()
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
        user_favorites = set(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    # رنگ‌های محصول
    colors = product.colors.all()
    
    context = {
        'product': product,
        'related_products': related_products,
        'comments': comments,
        'comment_form': comment_form,
        'is_favorite': is_favorite,
        'user_favorites': user_favorites,
        'colors': colors,
    }
    
    return render(request, 'products/singleProduct.html', context)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def add_comment(request, slug):
    """افزودن نظر به محصول"""
    product = get_object_or_404(Product, slug=slug)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.Product = product
        comment.author = request.user
        comment.save()
        
        messages.success(request, 'نظر شما با موفقیت ثبت شد')
        return redirect('product', slug=slug)
    else:
        messages.error(request, 'خطا در ثبت نظر')
        return redirect('product', slug=slug)


def search_products(request):
    """جستجوی محصولات با فیلتر و مرتب‌سازی"""
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(english_title__icontains=query)
        )
    else:
        products = Product.objects.none()
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # فیلتر بر اساس برند
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    
    # فیلتر بر اساس رنگ
    color_id = request.GET.get('color')
    if color_id:
        products = products.filter(colors__id=color_id)
    
    # فیلتر بر اساس قیمت
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except ValueError:
            pass
    
    # فیلتر فقط کالاهای موجود
    only_available = request.GET.get('only_available')
    if only_available == 'true':
        products = products.filter(stock__gt=0)
    
    # مرتب‌سازی
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'sales':
        products = products.order_by('-sales')
    elif sort_by == 'views':
        products = products.order_by('-views')
    elif sort_by == 'created_at':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-created_at')  # پیش‌فرض
    
    # محاسبه محدوده قیمت
    if products.exists():
        price_range = products.aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
    else:
        price_range = {'min_price': 0, 'max_price': 0}
    
    # دریافت دسته‌بندی‌های مناسب برای فیلتر (نه برای منوی اصلی)
    selected_category_obj = None
    if category_slug:
        try:
            selected_category_obj = Category.objects.get(slug=category_slug)
            filter_categories = selected_category_obj.get_children().order_by('name')
        except Category.DoesNotExist:
            filter_categories = Category.objects.filter(parent__isnull=True).exclude(slug='').order_by('name')
    else:
        filter_categories = Category.objects.filter(parent__isnull=True).exclude(slug='').order_by('name')
    
    # رنگ‌ها
    colors = Color.objects.all().order_by('name')
    brands = Brand.objects.filter(is_active=True).order_by('order', 'name')
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 محصول در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # بررسی favorite برای کاربران لاگین شده
    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    context = {
        'products': page_obj,
        'query': query,
        'user_favorites': user_favorites,
        'filter_categories': filter_categories,  # فقط برای فیلتر سمت راست
        'selected_category_obj': selected_category_obj,
        'colors': colors,
        'brands': brands,
        'selected_category': category_slug,
        'selected_brand': brand_slug,
        'selected_color': color_id,
        'price_range': price_range,
        'sort_by': sort_by,
        'only_available': only_available == 'true',
    }
    
    return render(request, 'products/searchResult.html', context)


def bestseller_products(request):
    """صفحه محصولات پرفروش‌ترین"""
    products = Product.objects.filter(sales__gt=0).order_by('-sales')
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # فیلتر بر اساس برند
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    
    # فیلتر بر اساس رنگ
    color_id = request.GET.get('color')
    if color_id:
        products = products.filter(colors__id=color_id)
    
    # فیلتر بر اساس قیمت
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except ValueError:
            pass
    
    # فیلتر فقط کالاهای موجود
    only_available = request.GET.get('only_available')
    if only_available == 'true':
        products = products.filter(stock__gt=0)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(english_title__icontains=search_query)
        )
    
    # محاسبه محدوده قیمت برای فیلتر
    price_range = products.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )
    
    # صفحه‌بندی
    paginator = Paginator(products, 12)  # 12 محصول در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # دریافت دسته‌بندی‌های مناسب برای فیلتر (نه برای منوی اصلی)
    selected_category_obj = None
    if category_slug:
        try:
            selected_category_obj = Category.objects.get(slug=category_slug)
            filter_categories = selected_category_obj.get_children().order_by('name')
        except Category.DoesNotExist:
            filter_categories = Category.objects.filter(parent__isnull=True).exclude(slug='').order_by('name')
    else:
        filter_categories = Category.objects.filter(parent__isnull=True).exclude(slug='').order_by('name')
    colors = Color.objects.distinct()
    brands = Brand.objects.filter(is_active=True).order_by('order', 'name')
    
    # بررسی favorite برای کاربران لاگین شده
    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))
    
    context = {
        'products': page_obj,
        'filter_categories': filter_categories,  # فقط برای فیلتر سمت راست
        'selected_category_obj': selected_category_obj,
        'colors': colors,
        'brands': brands,
        'selected_category': category_slug,
        'selected_brand': brand_slug,
        'selected_color': color_id,
        'search_query': search_query,
        'price_range': price_range,
        'sort_by': 'sales',  # مرتب‌سازی بر اساس فروش
        'user_favorites': user_favorites,
        'only_available': only_available == 'true',
        'page_title': 'پرفروش‌ترین محصولات',
    }
    
    return render(request, 'products/shop.html', context)
