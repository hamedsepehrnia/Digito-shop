from django.contrib import admin
from django.utils.html import format_html
from core.admin_utils import format_date_for_admin
from .models import About, AboutSection, ContactInfo, ContactMessage, FooterLink, FooterLinkGroup, SocialMedia, FooterSettings, AdminSettings, Banner


class AboutSectionInline(admin.TabularInline):
    """Inline for about us sections"""
    model = AboutSection
    extra = 1
    fields = ['title', 'content', 'order']


# Admin class for hidden model AboutSection (only displayed in advanced mode)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['about', 'title', 'order']
    list_filter = ['about']
    search_fields = ['about__title', 'title', 'content']
    list_editable = ['order']
    list_per_page = 25


class AboutAdmin(admin.ModelAdmin):
    """About us page management"""
    list_display = ['title', 'is_active', 'jalali_created']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['updated_at', 'jalali_created']
    inlines = [AboutSectionInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'content', 'image', 'is_active'),
            'description': '<strong>راهنمای سایز تصویر:</strong> سایز بهینه 1200x800 پیکسل (نسبت 3:2). فرمت پیشنهادی: JPG یا WebP'
        }),
        ('اطلاعات زمانی', {
            'fields': ('jalali_created', 'updated_at')
        }),
    )
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=False)
    jalali_created.short_description = 'تاریخ ایجاد'


class ContactInfoAdmin(admin.ModelAdmin):
    """Contact information management"""
    list_display = ['email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['email', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('اطلاعات تماس', {
            'fields': ('email', 'phone', 'address', 'postal_code', 'working_hours', 'map_url', 'is_active')
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        # Only one record can exist
        if ContactInfo.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False


class ContactMessageAdmin(admin.ModelAdmin):
    """Contact messages management"""
    list_display = ['name', 'phone', 'is_read', 'jalali_created']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'phone', 'message']
    readonly_fields = ['jalali_created']
    fieldsets = (
        ('اطلاعات پیام', {
            'fields': ('name', 'phone', 'message', 'is_read')
        }),
        ('اطلاعات زمانی', {
            'fields': ('jalali_created',)
        }),
    )
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ ارسال'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Mark messages as read"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} پیام به عنوان خوانده شده علامت‌گذاری شد.')
    mark_as_read.short_description = 'علامت‌گذاری به عنوان خوانده شده'
    
    def mark_as_unread(self, request, queryset):
        """Mark messages as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} پیام به عنوان خوانده نشده علامت‌گذاری شد.')
    mark_as_unread.short_description = 'علامت‌گذاری به عنوان خوانده نشده'


class FooterLinkAdmin(admin.ModelAdmin):
    """Footer links management"""
    list_display = ['title', 'url', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'url']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']


class FooterLinkInline(admin.TabularInline):
    """Inline for footer link group links"""
    model = FooterLinkGroup.links.through
    extra = 1
    verbose_name = "لینک"
    verbose_name_plural = "لینک‌ها"


class FooterLinkGroupAdmin(admin.ModelAdmin):
    """Footer link groups management"""
    list_display = ['title', 'order', 'is_active', 'get_links_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']
    filter_horizontal = ['links']
    
    def get_links_count(self, obj):
        return obj.links.filter(is_active=True).count()
    get_links_count.short_description = 'تعداد لینک‌ها'


class SocialMediaAdmin(admin.ModelAdmin):
    """Social media management"""
    list_display = ['platform', 'url', 'order', 'is_active', 'created_at']
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['url']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']


class FooterSettingsAdmin(admin.ModelAdmin):
    """Footer settings management"""
    list_display = ['is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('تنظیمات فوتر', {
            'fields': ('description', 'copyright_text', 'is_active')
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        # Only one record can exist
        if FooterSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False


class BannerAdmin(admin.ModelAdmin):
    """Site banners management"""
    list_display = ['get_image_preview', 'title', 'banner_type', 'order', 'is_active', 'jalali_created']
    list_filter = ['banner_type', 'is_active', 'created_at']
    search_fields = ['title']
    list_editable = ['order', 'is_active']
    readonly_fields = ['updated_at', 'jalali_created', 'get_image_preview']
    list_per_page = 25
    
    fieldsets = (
        ('اطلاعات بنر', {
            'fields': ('title', 'image', 'get_image_preview', 'link', 'banner_type', 'order', 'is_active'),
            'description': '<strong>راهنمای سایز تصویر:</strong><br>'
                          '• بنر اصلی (Hero Slider): 1920x384 پیکسل (نسبت 5:1) - برای نمایش در اسلایدر بالای صفحه<br>'
                          '• بنر کناری (Sidebar): 300x600 پیکسل (نسبت 1:2) - برای نمایش در کنار محصولات شگفت‌انگیز<br>'
                          '• بنر پایین صفحه: 1200x675 پیکسل (نسبت 16:9) - برای نمایش در بخش پایین صفحه<br>'
                          '• فرمت پیشنهادی: JPG یا WebP برای حجم کمتر'
        }),
        ('اطلاعات زمانی', {
            'fields': ('jalali_created', 'updated_at')
        }),
    )
    
    def get_image_preview(self, obj):
        if obj and obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "تصویری وجود ندارد"
    get_image_preview.short_description = "پیش‌نمایش"
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=False)
    jalali_created.short_description = 'تاریخ ایجاد'


class AdminSettingsAdmin(admin.ModelAdmin):
    """Admin panel settings management"""
    list_display = ['use_jalali_date', 'show_hidden_models', 'site_title', 'site_header', 'site_index_title']
    list_filter = ['use_jalali_date', 'show_hidden_models']
    readonly_fields = []
    fieldsets = (
        ('تنظیمات تاریخ', {
            'fields': ('use_jalali_date',)
        }),
        ('تنظیمات نمایش', {
            'fields': ('site_title', 'site_header', 'site_index_title', 'show_hidden_models'),
            'description': 'مدل‌های پنهان شده: تصاویر محصولات، مشخصات محصولات، آیتم‌های سفارش، آیتم‌های سبد خرید، کدهای تایید تلفن، بخش‌های درباره ما'
        }),
    )
    
    def has_add_permission(self, request):
        # Only one record can exist
        if AdminSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False
