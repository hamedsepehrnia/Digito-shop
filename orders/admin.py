from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'color', 'quantity', 'price', 'get_total_price']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,} تومان"
    get_total_price.short_description = 'جمع'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'get_final_price', 'jalali_created', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__phone', 'user__fullname']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'get_full_address']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('order_number', 'user', 'status', 'get_full_address')
        }),
        ('اطلاعات پرداخت', {
            'fields': ('payment_method', 'payment_status', 'total_price', 'shipping_cost')
        }),
        ('سایر', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )
    
    exclude = ['address']
    
    def get_final_price(self, obj):
        return f"{obj.get_final_price():,} تومان"
    get_final_price.short_description = 'جمع نهایی'
    
    def jalali_created(self, obj):
        return obj.jalali_created()
    jalali_created.short_description = 'تاریخ ثبت (شمسی)'
    
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
