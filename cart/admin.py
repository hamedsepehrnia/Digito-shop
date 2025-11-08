from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'created_at']
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'تعداد آیتم‌ها'
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,} تومان"
    get_total_price.short_description = 'جمع کل'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'color', 'quantity', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    
    def get_total_price(self, obj):
        return f"{obj.get_total_price():,} تومان"
    get_total_price.short_description = 'جمع'
