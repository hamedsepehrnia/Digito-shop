from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Product, ProductSpecification, ProductImage, Category, Color, Comment


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """مدیریت دسته‌بندی‌ها با قابلیت drag & drop"""
    list_display = ['tree_actions', 'indented_title', 'slug']
    list_display_links = ['indented_title']
    search_fields = ['name', 'slug']
    mptt_level_indent = 20


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'stock', 'sales', 'views', 'is_amazing', 'created_at']
    list_filter = ['category', 'is_amazing', 'created_at']
    search_fields = ['title', 'english_title', 'description']
    filter_horizontal = ['colors']
    inlines = [ProductImageInline, ProductSpecificationInline]
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'english_title', 'category', 'description')
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'stock', 'delivery_date')
        }),
        ('ویژگی‌ها', {
            'fields': ('colors', 'warranty_months', 'satisfaction_percent', 'is_amazing')
        }),
        ('آمار', {
            'fields': ('sales', 'views', 'created_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['Product', 'author', 'recommendation', 'bought_by_author', 'jalali_created', 'created_at']
    list_filter = ['recommendation', 'bought_by_author', 'created_at']
    search_fields = ['content', 'author__phone', 'Product__title']
    readonly_fields = ['created_at']
    
    def jalali_created(self, obj):
        return obj.jalali_created()
    jalali_created.short_description = 'تاریخ (شمسی)'
