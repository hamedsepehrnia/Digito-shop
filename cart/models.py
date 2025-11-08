from django.db import models
from accounts.models import MyUser
from products.models import Product, Color


class Cart(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='cart', verbose_name="کاربر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"
        ordering = ['-updated_at']

    def __str__(self):
        return f"سبد خرید {self.user.phone}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="سبد خرید")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="رنگ")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ افزودن")

    class Meta:
        unique_together = ['cart', 'product', 'color']
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.title} - {self.quantity} عدد"

    def get_total_price(self):
        return self.product.price * self.quantity
