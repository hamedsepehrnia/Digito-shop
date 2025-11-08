from django.contrib import admin
from .models import MyUser, Address, Favorite, PhoneOTP


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'fullname', 'province', 'city', 'is_active', 'is_admin']
    list_filter = ['is_active', 'is_admin', 'gender']
    search_fields = ['phone', 'fullname']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'city', 'province']
    list_filter = ['province', 'city']
    search_fields = ['user__phone', 'first_name', 'last_name']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__phone', 'product__title']


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'otp', 'created_at', 'expires_at', 'is_valid']
    list_filter = ['created_at']
    search_fields = ['phone_number']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'معتبر'
