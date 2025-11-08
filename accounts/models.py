import random


from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models



class MyUserManager(BaseUserManager):
    def create_user(self, phone=None, password=None, fullname="", age=None, province="", city="", date_of_birth=None, gender=""):
        if not phone:
            phone = "unknown" + str(random.randint(100000, 999999))  # مقدار جایگزین موقت
        user = self.model(
            phone=phone,
            fullname=fullname,
            age=age,
            province=province,
            city=city,
            gender=gender,
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, fullname="", age=None, province="", city="", date_of_birth=None):
        user = self.create_user(
            phone=phone,
            password=password,
            fullname=fullname,
            age=age,
            province=province,
            city=city,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True, verbose_name="شماره تلفن")
    fullname = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی", blank=True)
    age = models.PositiveSmallIntegerField(verbose_name="سن", null=True, blank=True)
    province = models.CharField(max_length=100, verbose_name="استان", blank=True)
    city = models.CharField(max_length=100, verbose_name="شهر", blank=True)
    gender_choices = (
        ('male', "مرد"),
        ('female', "زن")
    )
    gender = models.CharField(choices=gender_choices, null=True, blank=True, max_length=50, verbose_name="جنسیت")

    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    is_admin = models.BooleanField(default=False, verbose_name="مدیر است")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ['-id']

    objects = MyUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
    
    def get_full_name(self):
        """برگرداندن نام کامل کاربر"""
        return self.fullname if self.fullname else self.phone
    
    def get_short_name(self):
        """برگرداندن نام کوتاه کاربر"""
        return self.fullname if self.fullname else self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    otp = models.CharField(max_length=6, verbose_name="کد تایید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    expires_at = models.DateTimeField(verbose_name="تاریخ انقضا")

    class Meta:
        verbose_name = "کد تایید تلفن"
        verbose_name_plural = "کدهای تایید تلفن"
        ordering = ['-created_at']

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.phone_number} • {self.otp}"
class Address(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='addresses', verbose_name="کاربر")
    subject = models.CharField(max_length=50, null=True, blank=True, verbose_name="عنوان آدرس")
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    province = models.CharField(max_length=50, verbose_name="استان")
    city = models.CharField(max_length=50, verbose_name="شهر")
    address_details = models.CharField(max_length=50, verbose_name="جزئیات آدرس")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    postal_code = models.CharField(max_length=50, verbose_name="کد پستی")
    additional_info = models.CharField(max_length=50, verbose_name="اطلاعات اضافی", blank=True)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"
        ordering = ['-id']
    
    def __str__(self):
        address_parts = []
        if self.subject:
            address_parts.append(self.subject)
        address_parts.append(f"{self.province} - {self.city}")
        if self.address_details:
            address_parts.append(self.address_details)
        return " | ".join(address_parts)
    
    def get_full_address(self):
        """نمایش کامل آدرس با تمام جزئیات"""
        parts = []
        if self.subject:
            parts.append(f"عنوان: {self.subject}")
        parts.append(f"نام: {self.first_name} {self.last_name}")
        parts.append(f"آدرس: {self.province} - {self.city} - {self.address_details}")
        parts.append(f"کد پستی: {self.postal_code}")
        parts.append(f"تلفن: {self.phone_number}")
        if self.additional_info:
            parts.append(f"توضیحات: {self.additional_info}")
        return "\n".join(parts)


class Favorite(models.Model):
    """علاقه‌مندی‌های کاربر"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']
        verbose_name = 'علاقه‌مندی'
        verbose_name_plural = 'علاقه‌مندی‌ها'

    def __str__(self):
        return f"{self.user.phone} - {self.product.title}"