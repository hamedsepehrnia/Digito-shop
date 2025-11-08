from django.contrib import admin
from django.utils.html import format_html
from core.admin_utils import format_date_for_admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['product', 'color', 'quantity', 'price', 'get_total_price']
    readonly_fields = ['get_total_price']
    
    def get_total_price(self, obj):
        if obj.pk:
            return f"{obj.get_total_price():,} تومان"
        return "-"
    get_total_price.short_description = 'جمع'


# Admin class برای مدل پنهان OrderItem (فقط در حالت پیشرفته نمایش داده می‌شود)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'color', 'quantity', 'price', 'get_total_price', 'jalali_created']
    list_filter = ['order__status', 'created_at']
    search_fields = ['order__order_number', 'product__title']
    readonly_fields = ['created_at', 'jalali_created', 'get_total_price']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,} تومان"
    get_total_price.short_description = 'جمع کل'
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ ثبت'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'get_status_display', 'get_payment_status_display', 'get_final_price', 'jalali_created']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__phone', 'user__fullname']
    readonly_fields = ['order_number', 'updated_at', 'jalali_created', 'jalali_updated', 'get_full_address']
    inlines = [OrderItemInline]
    list_editable = ['status']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('order_number', 'user', 'status', 'get_full_address')
        }),
        ('اطلاعات پرداخت', {
            'fields': ('payment_method', 'payment_status', 'total_price', 'shipping_cost')
        }),
        ('سایر', {
            'fields': ('notes', 'jalali_created', 'jalali_updated')
        }),
    )
    
    exclude = ['address']
    
    def get_status_display(self, obj):
        status_colors = {
            'pending': '#f59e0b',
            'paid': '#10b981',
            'processing': '#3b82f6',
            'shipped': '#8b5cf6',
            'delivered': '#059669',
            'cancelled': '#ef4444',
        }
        color = status_colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status_display.short_description = 'وضعیت'
    
    def get_payment_status_display(self, obj):
        if obj.payment_status:
            return format_html('<span style="color: #10b981;">✓ پرداخت شده</span>')
        return format_html('<span style="color: #ef4444;">✗ پرداخت نشده</span>')
    get_payment_status_display.short_description = 'وضعیت پرداخت'
    
    def get_final_price(self, obj):
        return f"{obj.get_final_price():,} تومان"
    get_final_price.short_description = 'جمع نهایی'
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ ثبت'
    
    def jalali_updated(self, obj):
        return format_date_for_admin(obj.updated_at, include_time=True)
    jalali_updated.short_description = 'آخرین بروزرسانی'
    
    def get_full_address(self, obj):
        """نمایش کامل آدرس با تمام جزئیات"""
        if obj.address:
            address_text = obj.address.get_full_address()
            # تبدیل خطوط جدید به <br> برای نمایش در HTML
            address_html = address_text.replace('\n', '<br>')
            return format_html(address_html)
        return "آدرسی ثبت نشده است"
    get_full_address.short_description = 'جزئیات آدرس'


# OrderItem از منوی ادمین پنهان شده است
# برای مشاهده آیتم‌های سفارش، از طریق Order می‌توانید به آنها دسترسی داشته باشید
