from django.contrib import admin
from django.utils.html import format_html
from core.admin_utils import format_date_for_admin
from .models import MyUser, Address, Favorite, PhoneOTP


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'fullname', 'province', 'city', 'gender', 'is_active', 'is_admin', 'get_orders_count']
    list_filter = ['is_active', 'is_admin', 'gender', 'province', 'city']
    search_fields = ['phone', 'fullname']
    readonly_fields = ['last_login']
    list_editable = ['is_active']
    list_per_page = 25
    
    fieldsets = (
        ('اطلاعات کاربری', {
            'fields': ('phone', 'fullname', 'gender', 'age')
        }),
        ('اطلاعات مکانی', {
            'fields': ('province', 'city')
        }),
        ('دسترسی‌ها', {
            'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('اطلاعات ورود', {
            'fields': ('last_login',)
        }),
    )
    
    def get_orders_count(self, obj):
        count = obj.orders.count()
        return count if count > 0 else "-"
    get_orders_count.short_description = "تعداد سفارش‌ها"


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'get_full_name', 'province', 'city', 'postal_code']
    list_filter = ['province', 'city']
    search_fields = ['user__phone', 'user__fullname', 'first_name', 'last_name', 'subject', 'postal_code']
    readonly_fields = ['get_full_address_display']
    list_per_page = 25
    
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user',)
        }),
        ('اطلاعات آدرس', {
            'fields': ('subject', 'first_name', 'last_name', 'province', 'city', 'address_details', 'postal_code', 'phone_number', 'additional_info')
        }),
        ('نمایش کامل آدرس', {
            'fields': ('get_full_address_display',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = "نام و نام خانوادگی"
    
    def get_full_address_display(self, obj):
        return obj.get_full_address().replace('\n', '<br>')
    get_full_address_display.short_description = "آدرس کامل"
    get_full_address_display.allow_tags = True


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'get_product_price', 'jalali_created']
    list_filter = ['created_at']
    search_fields = ['user__phone', 'user__fullname', 'product__title']
    readonly_fields = ['jalali_created']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def get_product_price(self, obj):
        return f"{obj.product.price:,} تومان" if obj.product else "-"
    get_product_price.short_description = "قیمت محصول"
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ افزودن'


class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'otp', 'is_valid', 'jalali_created', 'jalali_expires_at']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['phone_number', 'otp']
    readonly_fields = ['jalali_created', 'jalali_expires_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'معتبر'
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ ایجاد'
    
    def jalali_expires_at(self, obj):
        return format_date_for_admin(obj.expires_at, include_time=True)
    jalali_expires_at.short_description = 'تاریخ انقضا'
