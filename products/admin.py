from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin
from core.admin_utils import format_date_for_admin
from .models import Product, ProductSpecification, ProductImage, Category, Color, Comment, Brand


class CategoryAdmin(DraggableMPTTAdmin):
    """Category management with drag & drop capability"""
    list_display = ['tree_actions', 'indented_title', 'get_image_preview', 'slug']
    list_display_links = ['indented_title']
    search_fields = ['name', 'slug']
    mptt_level_indent = 20
    readonly_fields = ['get_image_preview']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'parent', 'image', 'get_image_preview'),
            'description': '<strong>راهنمای سایز تصویر:</strong> سایز بهینه 200x200 پیکسل (مربع). فرمت پیشنهادی: PNG یا JPG'
        }),
    )
    
    def get_image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "تصویری وجود ندارد"
    get_image_preview.short_description = "پیش‌نمایش تصویر"


class BrandAdmin(admin.ModelAdmin):
    list_display = ['get_logo_preview', 'name', 'slug', 'order', 'is_active', 'get_products_count', 'jalali_created']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'jalali_created', 'get_logo_preview']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25
    
    fieldsets = (
        ('اطلاعات برند', {
            'fields': ('name', 'slug', 'logo', 'get_logo_preview', 'order', 'is_active')
        }),
        ('اطلاعات زمانی', {
            'fields': ('jalali_created',)
        }),
    )
    
    def get_logo_preview(self, obj):
        if obj and obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.logo.url)
        return "لوگویی وجود ندارد"
    get_logo_preview.short_description = "پیش‌نمایش لوگو"
    
    def get_products_count(self, obj):
        count = obj.products.count()
        return count if count > 0 else "-"
    get_products_count.short_description = "تعداد محصولات"
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=False)
    jalali_created.short_description = 'تاریخ ایجاد'


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code', 'get_color_preview']
    search_fields = ['name', 'hex_code']
    list_editable = ['hex_code']
    
    def get_color_preview(self, obj):
        if obj.hex_code:
            return format_html(
                '<div style="width: 30px; height: 30px; background-color: {}; border: 1px solid #ccc; border-radius: 4px;"></div>',
                obj.hex_code
            )
        return "-"
    get_color_preview.short_description = "پیش‌نمایش رنگ"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt', 'get_image_preview']
    readonly_fields = ['get_image_preview']
    verbose_name = "تصویر محصول"
    verbose_name_plural = "تصاویر محصولات"
    classes = ['collapse']  # For better display
    
    def get_image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "تصویری وجود ندارد"
    get_image_preview.short_description = "پیش‌نمایش"


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    fields = ['key', 'value']


# Admin classes for hidden models (only displayed in advanced mode)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'get_image_preview', 'alt', 'id']
    list_filter = ['product__category']
    search_fields = ['product__title', 'alt']
    readonly_fields = ['get_image_preview']
    list_per_page = 25
    
    def get_image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "تصویری وجود ندارد"
    get_image_preview.short_description = "پیش‌نمایش"


class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']
    list_filter = ['product__category']
    search_fields = ['product__title', 'key', 'value']
    list_per_page = 25


class ProductAdmin(admin.ModelAdmin):
    list_display = ['get_image_preview', 'title', 'category', 'get_price_display', 'stock', 'sales', 'views', 'is_amazing', 'jalali_created']
    list_filter = ['category', 'brand', 'is_amazing', 'created_at', 'stock']
    search_fields = ['title', 'english_title', 'description', 'slug']
    filter_horizontal = ['colors']
    inlines = [ProductImageInline, ProductSpecificationInline]
    readonly_fields = ['jalali_created']
    list_editable = ['stock', 'is_amazing']
    date_hierarchy = 'created_at'
    list_per_page = 25
    list_display_links = ['title']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'english_title', 'category', 'brand', 'description'),
            'description': '<strong>نکته:</strong> برای افزودن تصاویر محصول، از بخش "تصاویر محصولات" در پایین صفحه استفاده کنید.'
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'stock', 'delivery_date')
        }),
        ('ویژگی‌ها', {
            'fields': ('colors', 'warranty_months', 'satisfaction_percent', 'is_amazing')
        }),
        ('آمار', {
            'fields': ('sales', 'views', 'jalali_created')
        }),
    )
    
    def get_image_preview(self, obj):
        if obj.images.first():
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.images.first().image.url)
        return "بدون تصویر"
    get_image_preview.short_description = "تصویر"
    
    def get_price_display(self, obj):
        return f"{obj.price:,} تومان"
    get_price_display.short_description = "قیمت"
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=False)
    jalali_created.short_description = 'تاریخ ثبت'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['Product', 'author', 'get_content_preview', 'recommendation', 'bought_by_author', 'jalali_created']
    list_filter = ['recommendation', 'bought_by_author', 'created_at']
    search_fields = ['content', 'author__phone', 'author__fullname', 'Product__title']
    readonly_fields = ['jalali_created']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات نظر', {
            'fields': ('Product', 'author', 'content', 'recommendation', 'bought_by_author')
        }),
        ('اطلاعات زمانی', {
            'fields': ('jalali_created',)
        }),
    )
    
    def get_content_preview(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content
    get_content_preview.short_description = "محتوا"
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ ثبت'
