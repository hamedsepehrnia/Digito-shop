from django.db import models
from django.utils.text import slugify
from persiantools.jdatetime import JalaliDateTime
from accounts.models import MyUser


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    ]

    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    content = models.TextField(verbose_name="محتوا")
    excerpt = models.TextField(max_length=500, blank=True, verbose_name="خلاصه")
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, verbose_name="نویسنده")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی")
    
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="تصویر")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    views = models.PositiveIntegerField(default=0, verbose_name="بازدید")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def jalali_created(self):
        return JalaliDateTime(self.created_at).strftime('%Y/%m/%d')

    def jalali_published(self):
        if self.published_at:
            return JalaliDateTime(self.published_at).strftime('%Y/%m/%d')
        return None


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="پست")
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="نویسنده")
    content = models.TextField(verbose_name="محتوا")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f"نظر {self.author.phone} برای {self.post.title}"

    def jalali_created(self):
        return JalaliDateTime(self.created_at).strftime('%Y/%m/%d - %H:%M')
