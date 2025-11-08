from django.db import models
from django.utils import timezone
from persiantools.jdatetime import JalaliDateTime
from accounts.models import MyUser, Address
from products.models import Product, Color


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('online', 'پرداخت آنلاین'),
        ('cash', 'پرداخت در محل'),
    ]

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True, verbose_name="شماره سفارش")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name="آدرس")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='online', verbose_name="روش پرداخت")
    payment_status = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")
    
    total_price = models.PositiveIntegerField(verbose_name="جمع کل")
    shipping_cost = models.PositiveIntegerField(default=0, verbose_name="هزینه ارسال")
    
    notes = models.TextField(blank=True, verbose_name="یادداشت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'

    def __str__(self):
        return f"سفارش {self.order_number}"

    def get_final_price(self):
        total_price = self.total_price or 0
        shipping_cost = self.shipping_cost or 0
        return total_price + shipping_cost

    def jalali_created(self):
        return JalaliDateTime(self.created_at).strftime('%Y/%m/%d - %H:%M')

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            self.order_number = ''.join(random.choices(string.digits, k=10))
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="تعداد")
    price = models.PositiveIntegerField(verbose_name="قیمت واحد")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        product_name = self.product.title if self.product else "محصول حذف شده"
        return f"{product_name} - {self.quantity} عدد"

    def get_total_price(self):
        price = self.price or 0
        quantity = self.quantity or 0
        return price * quantity
