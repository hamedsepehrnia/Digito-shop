from django.db import models
from persiantools.jdatetime import JalaliDateTime


class About(models.Model):
    """مدل برای صفحه درباره ما"""
    title = models.CharField(max_length=255, verbose_name="عنوان")
    content = models.TextField(verbose_name="محتوا")
    image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="عکس")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    
    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def jalali_created(self):
        return JalaliDateTime(self.created_at).strftime('%Y/%m/%d')


class AboutSection(models.Model):
    """بخش‌های مختلف صفحه درباره ما"""
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='sections', verbose_name="درباره ما")
    title = models.CharField(max_length=255, verbose_name="عنوان بخش")
    content = models.TextField(verbose_name="محتوا")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    
    class Meta:
        verbose_name = "بخش درباره ما"
        verbose_name_plural = "بخش‌های درباره ما"
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.about.title} - {self.title}"


class ContactInfo(models.Model):
    """اطلاعات تماس با ما"""
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن")
    address = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="کد پستی")
    working_hours = models.CharField(max_length=100, verbose_name="ساعات کاری")
    map_url = models.URLField(blank=True, null=True, verbose_name="لینک نقشه")
    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    
    class Meta:
        verbose_name = "اطلاعات تماس"
        verbose_name_plural = "اطلاعات تماس"
    
    def __str__(self):
        return f"اطلاعات تماس - {self.email}"
    
    def save(self, *args, **kwargs):
        # فقط یک رکورد فعال می‌تواند وجود داشته باشد
        if self.is_active:
            ContactInfo.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """پیام‌های ارسالی از فرم تماس با ما"""
    name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن")
    message = models.TextField(verbose_name="پیام")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    
    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    def jalali_created(self):
        return JalaliDateTime(self.created_at).strftime('%Y/%m/%d - %H:%M')


class FooterLink(models.Model):
    """لینک‌های فوتر"""
    title = models.CharField(max_length=255, verbose_name="عنوان")
    url = models.CharField(max_length=500, verbose_name="لینک")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "لینک فوتر"
        verbose_name_plural = "لینک‌های فوتر"
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.title


class FooterLinkGroup(models.Model):
    """گروه‌های لینک فوتر"""
    title = models.CharField(max_length=255, verbose_name="عنوان گروه")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    links = models.ManyToManyField(FooterLink, related_name='groups', verbose_name="لینک‌ها")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "گروه لینک فوتر"
        verbose_name_plural = "گروه‌های لینک فوتر"
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.title


class SocialMedia(models.Model):
    """شبکه‌های اجتماعی"""
    SOCIAL_CHOICES = [
        ('telegram', 'تلگرام'),
        ('whatsapp', 'واتساپ'),
        ('instagram', 'اینستاگرام'),
        ('twitter', 'توییتر'),
        ('linkedin', 'لینکدین'),
        ('youtube', 'یوتیوب'),
        ('aparat', 'آپارات'),
    ]
    
    platform = models.CharField(max_length=50, choices=SOCIAL_CHOICES, verbose_name="پلتفرم")
    url = models.URLField(verbose_name="لینک")
    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه‌های اجتماعی"
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.get_platform_display()


class FooterSettings(models.Model):
    """تنظیمات فوتر"""
    description = models.TextField(verbose_name="توضیحات فوتر", blank=True, null=True)
    copyright_text = models.CharField(max_length=500, default="تمامی حقوق توسط تیم برنامه نویسی امیران محفوظ است.", verbose_name="متن کپی‌رایت")
    is_active = models.BooleanField(default=True, verbose_name="فعال است")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    
    class Meta:
        verbose_name = "تنظیمات فوتر"
        verbose_name_plural = "تنظیمات فوتر"
    
    def __str__(self):
        return "تنظیمات فوتر"
    
    def save(self, *args, **kwargs):
        # فقط یک رکورد فعال می‌تواند وجود داشته باشد
        if self.is_active:
            FooterSettings.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
