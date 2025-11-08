"""
Django Admin Panel Customization
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.conf import settings
from core.models import AdminSettings


class DigitoAdminSite(AdminSite):
    """Custom admin site for Digito"""
    site_header = settings.ADMIN_SITE_HEADER
    site_title = settings.ADMIN_SITE_TITLE
    index_title = settings.ADMIN_SITE_INDEX_TITLE
    
    def each_context(self, request):
        """Add settings to context for all admin pages"""
        context = super().each_context(request)
        try:
            settings = AdminSettings.get_settings()
            context['admin_settings'] = settings
            # Apply settings to site_header and site_title
            if settings.site_header:
                self.site_header = settings.site_header
            if settings.site_title:
                self.site_title = settings.site_title
            if settings.site_index_title:
                self.index_title = settings.site_index_title
        except:
            context['admin_settings'] = AdminSettings.get_settings()
        return context


# Create custom AdminSite instance
admin_site = DigitoAdminSite(name='digito_admin')

# Import models and Admin classes
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


# Function to register/unregister hidden models
def update_hidden_models():
    """Update hidden models based on settings"""
    try:
        settings = AdminSettings.get_settings()
        show_hidden = settings.show_hidden_models
    except Exception:
        show_hidden = False
    
    # List of hidden models and their admin classes
    hidden_models = [
        (ProductImage, ProductImageAdmin),
        (ProductSpecification, ProductSpecificationAdmin),
        (PhoneOTP, PhoneOTPAdmin),
        (AboutSection, AboutSectionAdmin),
        (OrderItem, OrderItemAdmin),
        (CartItem, CartItemAdmin),
    ]
    
    # Register or unregister hidden models
    for model, admin_class in hidden_models:
        if show_hidden:
            # Register if not already registered
            if not admin_site.is_registered(model):
                admin_site.register(model, admin_class)
        else:
            # Unregister if already registered
            if admin_site.is_registered(model):
                admin_site.unregister(model)


# Function to register main models (always displayed)
def register_main_models():
    """Register main models in admin_site"""
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


# Register main models
register_main_models()

# Update hidden models
update_hidden_models()

