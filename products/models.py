from persiantools.jdatetime import JalaliDateTime
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from mptt.fields import TreeForeignKey as MPTTTreeForeignKey
from accounts.models import MyUser
from slugify import slugify as slugify_persian


class Category(MPTTModel):
    """Category model with tree structure using django-mptt"""
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True, verbose_name="اسلاگ")
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name="تصویر",
        help_text="سایز بهینه: 200x200 پیکسل (مربع). فرمت پیشنهادی: PNG یا JPG"
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="دسته‌بندی والد"
    )
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
    
    def get_full_slug(self):
        """Generate full slug path from root to current category"""
        slugs = []
        current = self
        while current:
            if current.slug:
                slugs.insert(0, current.slug)
            current = current.parent
        return '/'.join(slugs)
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            base_slug = slugify_persian(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    """Product brand model"""
    name = models.CharField(max_length=100, verbose_name="نام برند")
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True, verbose_name="اسلاگ")
    logo = models.ImageField(
        upload_to='brands/', 
        verbose_name="لوگو",
        help_text="سایز بهینه: 200x200 پیکسل (مربع). فرمت پیشنهادی: PNG با پس‌زمینه شفاف"
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            base_slug = slugify_persian(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Color(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام رنگ")
    hex_code = models.CharField(max_length=7, verbose_name="کد رنگ")  # e.g., '#000000'

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان محصول")
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True, verbose_name="اسلاگ")
    english_title = models.CharField(max_length=255, blank=True, verbose_name="عنوان انگلیسی")
    description = models.TextField(verbose_name="توضیحات محصول")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته‌بندی", related_name='products')
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="برند"
    )
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی انبار")
    is_amazing = models.BooleanField(default=False, verbose_name="شگفت‌انگیز است")
    sales = models.IntegerField(verbose_name='فروش ها', default=0)
    views = models.IntegerField(verbose_name='بازدید ها', default=0)
    colors = models.ManyToManyField(Color, related_name='products', verbose_name="رنگ‌ها")
    warranty_months = models.PositiveSmallIntegerField(default=18, verbose_name="گارانتی (ماه)")
    satisfaction_percent = models.PositiveSmallIntegerField(default=100, verbose_name="درصد رضایت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    delivery_date = models.PositiveSmallIntegerField(default=0, verbose_name='ارسال طی ... روز کاری')

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-created_at']

    def get_full_slug(self):
        """Generate full slug path of product category"""
        if self.category:
            return self.category.get_full_slug()
        return ''
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            base_slug = slugify_persian(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="محصول")
    image = models.ImageField(
        upload_to='products/gallery/', 
        verbose_name="تصویر",
        help_text="سایز بهینه: 800x800 پیکسل (مربع) یا 800x600 پیکسل (نسبت 4:3). فرمت پیشنهادی: JPG یا WebP"
    )
    alt = models.CharField(max_length=255, blank=True, verbose_name="متن جایگزین")

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصولات"
        ordering = ['id']

    def __str__(self):
        return f"تصویر {self.product.title}"


class ProductSpecification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='specs', verbose_name="محصول")
    key = models.CharField(max_length=100, verbose_name="ویژگی")
    value = models.CharField(max_length=255, verbose_name="مقدار")

    class Meta:
        verbose_name = "مشخصات محصول"
        verbose_name_plural = "مشخصات محصولات"
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.value}"


class Comment(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="محصول")
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments', verbose_name="نویسنده")
    recommendation = models.BooleanField(default=False, verbose_name="توصیه می‌کند")
    bought_by_author = models.BooleanField(default=False, verbose_name="خریداری شده توسط نویسنده")
    content = models.TextField(verbose_name="محتوا")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "نظر محصول"
        verbose_name_plural = "نظرات محصولات"
        ordering = ['-created_at']

    def jalali_created(self):
        return JalaliDateTime(self.created_at).strftime('%Y/%m/%d - %H:%M')

    def __str__(self):
        return f"نظر {self.author.phone} برای {self.Product.title}"
