from persiantools.jdatetime import JalaliDateTime
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from mptt.fields import TreeForeignKey as MPTTTreeForeignKey
from accounts.models import MyUser
from slugify import slugify as slugify_persian


class Category(MPTTModel):
    """مدل دسته‌بندی با ساختار درختی با استفاده از django-mptt"""
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True, verbose_name="اسلاگ")
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
        """تولید مسیر کامل slug از ریشه تا دسته‌بندی فعلی"""
        slugs = []
        current = self
        while current:
            if current.slug:
                slugs.insert(0, current.slug)
            current = current.parent
        return '/'.join(slugs)
    
    def save(self, *args, **kwargs):
        """تولید خودکار slug در صورت عدم وجود"""
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


class Color(models.Model):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)  # مثلا '#000000'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان محصول")
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True, verbose_name="اسلاگ")
    english_title = models.CharField(max_length=255, blank=True, verbose_name="عنوان انگلیسی")
    description = models.TextField(verbose_name="توضیحات محصول")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته‌بندی", related_name='products')
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی انبار")
    is_amazing = models.BooleanField(default=False, verbose_name="شگفت‌انگیز است")
    sales = models.IntegerField(verbose_name='فروش ها', default=0)
    views = models.IntegerField(verbose_name='بازدید ها', default=0)
    colors = models.ManyToManyField(Color, related_name='products')
    warranty_months = models.PositiveSmallIntegerField(default=18, verbose_name="گارانتی (ماه)")
    satisfaction_percent = models.PositiveSmallIntegerField(default=100, verbose_name="درصد رضایت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    delivery_date = models.PositiveSmallIntegerField(default=0, verbose_name='ارسال طی ... روز کاری')

    def get_full_slug(self):
        """تولید مسیر کامل slug دسته‌بندی محصول"""
        if self.category:
            return self.category.get_full_slug()
        return ''
    
    def save(self, *args, **kwargs):
        """تولید خودکار slug در صورت عدم وجود"""
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt = models.CharField(max_length=255, blank=True)


class ProductSpecification(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='specs')
    key = models.CharField(max_length=100, verbose_name="ویژگی")
    value = models.CharField(max_length=255, verbose_name="مقدار")

    def __str__(self):
        return f"{self.key}: {self.value}"


class Comment(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    recommendation = models.BooleanField(default=False)
    bought_by_author = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def jalali_created(self):
        return JalaliDateTime(self.created_at).strftime('%Y/%m/%d - %H:%M')

    def __str__(self):
        return self.content
