from django.contrib import admin
from .models import About, AboutSection, ContactInfo, ContactMessage, FooterLink, FooterLinkGroup, SocialMedia, FooterSettings


class AboutSectionInline(admin.TabularInline):
    """Inline برای بخش‌های درباره ما"""
    model = AboutSection
    extra = 1
    fields = ['title', 'content', 'order']


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """مدیریت صفحه درباره ما"""
    list_display = ['title', 'is_active', 'jalali_created', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AboutSectionInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'content', 'image', 'is_active')
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def jalali_created(self, obj):
        return obj.jalali_created()
    jalali_created.short_description = 'تاریخ (شمسی)'


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """مدیریت اطلاعات تماس"""
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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """مدیریت پیام‌های تماس"""
    list_display = ['name', 'phone', 'is_read', 'jalali_created', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'phone', 'message']
    readonly_fields = ['created_at', 'jalali_created']
    fieldsets = (
        ('اطلاعات پیام', {
            'fields': ('name', 'phone', 'message', 'is_read')
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at', 'jalali_created')
        }),
    )
    
    def jalali_created(self, obj):
        return obj.jalali_created()
    jalali_created.short_description = 'تاریخ (شمسی)'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """علامت‌گذاری پیام‌ها به عنوان خوانده شده"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} پیام به عنوان خوانده شده علامت‌گذاری شد.')
    mark_as_read.short_description = 'علامت‌گذاری به عنوان خوانده شده'
    
    def mark_as_unread(self, request, queryset):
        """علامت‌گذاری پیام‌ها به عنوان خوانده نشده"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} پیام به عنوان خوانده نشده علامت‌گذاری شد.')
    mark_as_unread.short_description = 'علامت‌گذاری به عنوان خوانده نشده'


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    """مدیریت لینک‌های فوتر"""
    list_display = ['title', 'url', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'url']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']


class FooterLinkInline(admin.TabularInline):
    """Inline برای لینک‌های گروه فوتر"""
    model = FooterLinkGroup.links.through
    extra = 1
    verbose_name = "لینک"
    verbose_name_plural = "لینک‌ها"


@admin.register(FooterLinkGroup)
class FooterLinkGroupAdmin(admin.ModelAdmin):
    """مدیریت گروه‌های لینک فوتر"""
    list_display = ['title', 'order', 'is_active', 'get_links_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']
    filter_horizontal = ['links']
    
    def get_links_count(self, obj):
        return obj.links.filter(is_active=True).count()
    get_links_count.short_description = 'تعداد لینک‌ها'


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    """مدیریت شبکه‌های اجتماعی"""
    list_display = ['platform', 'url', 'order', 'is_active', 'created_at']
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['url']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']


@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    """مدیریت تنظیمات فوتر"""
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
        # فقط یک رکورد می‌تواند وجود داشته باشد
        if FooterSettings.objects.exists():
            return False
        return super().has_add_permission(request)
