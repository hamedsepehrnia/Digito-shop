from django.contrib import admin
from core.admin_utils import format_date_for_admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'color', 'quantity', 'get_total_price']
    readonly_fields = ['get_total_price']
    
    def get_total_price(self, obj):
        if obj.pk:
            return f"{obj.get_total_price():,} تومان"
        return "-"
    get_total_price.short_description = 'جمع'


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'jalali_updated']
    search_fields = ['user__phone', 'user__fullname']
    readonly_fields = ['updated_at', 'jalali_created', 'jalali_updated']
    inlines = [CartItemInline]
    list_per_page = 25
    
    fieldsets = (
        ('اطلاعات سبد خرید', {
            'fields': ('user', 'jalali_created', 'jalali_updated')
        }),
    )
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'تعداد آیتم‌ها'
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,} تومان"
    get_total_price.short_description = 'جمع کل'
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ ایجاد'
    
    def jalali_updated(self, obj):
        return format_date_for_admin(obj.updated_at, include_time=True)
    jalali_updated.short_description = 'آخرین بروزرسانی'


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'color', 'quantity', 'get_total_price', 'jalali_created']
    list_filter = ['created_at', 'color']
    search_fields = ['cart__user__phone', 'product__title']
    readonly_fields = ['created_at', 'jalali_created']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,} تومان"
    get_total_price.short_description = 'جمع'
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ افزودن'
