"""
سفارشی‌سازی پنل ادمین Django
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.conf import settings
from core.models import AdminSettings


class DigitoAdminSite(AdminSite):
    """سایت ادمین سفارشی برای دیجیتو"""
    site_header = settings.ADMIN_SITE_HEADER
    site_title = settings.ADMIN_SITE_TITLE
    index_title = settings.ADMIN_SITE_INDEX_TITLE
    
    def each_context(self, request):
        """افزودن تنظیمات به context تمام صفحات admin"""
        context = super().each_context(request)
        try:
            settings = AdminSettings.get_settings()
            context['admin_settings'] = settings
            # اعمال تنظیمات به site_header و site_title
            if settings.site_header:
                self.site_header = settings.site_header
            if settings.site_title:
                self.site_title = settings.site_title
            if settings.site_index_title:
                self.index_title = settings.site_index_title
        except:
            context['admin_settings'] = AdminSettings.get_settings()
        return context


# ایجاد instance سفارشی از AdminSite
admin_site = DigitoAdminSite(name='digito_admin')

# Import مدل‌ها و Admin classes
from products.admin import CategoryAdmin, ColorAdmin, ProductAdmin, CommentAdmin, ProductImageAdmin, ProductSpecificationAdmin, BrandAdmin
from products.models import Category, Color, Product, Comment, ProductImage, ProductSpecification, Brand
from accounts.admin import MyUserAdmin, AddressAdmin, FavoriteAdmin, PhoneOTPAdmin
from accounts.models import MyUser, Address, Favorite, PhoneOTP
from blog.admin import CategoryAdmin as BlogCategoryAdmin, PostAdmin, CommentAdmin as BlogCommentAdmin
from blog.models import Category as BlogCategory, Post, Comment as BlogComment
from core.admin import AboutAdmin, ContactInfoAdmin, ContactMessageAdmin, FooterLinkAdmin, FooterLinkGroupAdmin, SocialMediaAdmin, FooterSettingsAdmin, AdminSettingsAdmin, AboutSectionAdmin, BannerAdmin
from core.models import About, ContactInfo, ContactMessage, FooterLink, FooterLinkGroup, SocialMedia, FooterSettings, AboutSection, Banner
from orders.admin import OrderAdmin, OrderItemAdmin
from orders.models import Order, OrderItem
from cart.admin import CartAdmin, CartItemAdmin
from cart.models import Cart, CartItem


# تابع برای ثبت/لغو ثبت مدل‌های پنهان
def update_hidden_models():
    """به‌روزرسانی مدل‌های پنهان بر اساس تنظیمات"""
    try:
        settings = AdminSettings.get_settings()
        show_hidden = settings.show_hidden_models
    except Exception:
        show_hidden = False
    
    # لیست مدل‌های پنهان و admin classes آنها
    hidden_models = [
        (ProductImage, ProductImageAdmin),
        (ProductSpecification, ProductSpecificationAdmin),
        (PhoneOTP, PhoneOTPAdmin),
        (AboutSection, AboutSectionAdmin),
        (OrderItem, OrderItemAdmin),
        (CartItem, CartItemAdmin),
    ]
    
    # ثبت یا لغو ثبت مدل‌های پنهان
    for model, admin_class in hidden_models:
        if show_hidden:
            # اگر قبلاً ثبت نشده، ثبت کن
            if not admin_site.is_registered(model):
                admin_site.register(model, admin_class)
        else:
            # اگر ثبت شده، لغو ثبت کن
            if admin_site.is_registered(model):
                admin_site.unregister(model)


# تابع برای ثبت مدل‌های اصلی (همیشه نمایش داده می‌شوند)
def register_main_models():
    """ثبت مدل‌های اصلی در admin_site"""
    # Products
    admin_site.register(Category, CategoryAdmin)
    admin_site.register(Brand, BrandAdmin)
    admin_site.register(Color, ColorAdmin)
    admin_site.register(Product, ProductAdmin)
    admin_site.register(Comment, CommentAdmin)
    
    # Accounts
    admin_site.register(MyUser, MyUserAdmin)
    admin_site.register(Address, AddressAdmin)
    admin_site.register(Favorite, FavoriteAdmin)
    
    # Blog
    admin_site.register(BlogCategory, BlogCategoryAdmin)
    admin_site.register(Post, PostAdmin)
    admin_site.register(BlogComment, BlogCommentAdmin)
    
    # Core
    admin_site.register(About, AboutAdmin)
    admin_site.register(ContactInfo, ContactInfoAdmin)
    admin_site.register(ContactMessage, ContactMessageAdmin)
    admin_site.register(FooterLink, FooterLinkAdmin)
    admin_site.register(FooterLinkGroup, FooterLinkGroupAdmin)
    admin_site.register(SocialMedia, SocialMediaAdmin)
    admin_site.register(FooterSettings, FooterSettingsAdmin)
    admin_site.register(AdminSettings, AdminSettingsAdmin)
    admin_site.register(Banner, BannerAdmin)
    
    # Orders
    admin_site.register(Order, OrderAdmin)
    
    # Cart
    admin_site.register(Cart, CartAdmin)


# ثبت مدل‌های اصلی
register_main_models()

# به‌روزرسانی مدل‌های پنهان
update_hidden_models()

