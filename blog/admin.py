from django.contrib import admin
from core.admin_utils import format_date_for_admin
from .models import Post, Category, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'content', 'created_at', 'is_approved']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'jalali_created']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'updated_at', 'published_at']
    inlines = [CommentInline]
    actions = ['publish_posts', 'draft_posts']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('محتوا', {
            'fields': ('excerpt', 'content', 'image'),
            'description': '<strong>راهنمای سایز تصویر:</strong> سایز بهینه 1200x600 پیکسل (نسبت 2:1) یا 1200x800 پیکسل (نسبت 3:2). فرمت پیشنهادی: JPG یا WebP'
        }),
        ('آمار', {
            'fields': ('views', 'created_at', 'updated_at', 'published_at')
        }),
    )
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=False)
    jalali_created.short_description = 'تاریخ ایجاد'
    
    def publish_posts(self, request, queryset):
        """انتشار پست‌های انتخاب شده"""
        from django.utils import timezone
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} پست با موفقیت منتشر شد.')
    publish_posts.short_description = 'انتشار پست‌های انتخاب شده'
    
    def draft_posts(self, request, queryset):
        """برگرداندن پست‌های انتخاب شده به پیش‌نویس"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} پست به پیش‌نویس برگردانده شد.')
    draft_posts.short_description = 'برگرداندن به پیش‌نویس'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_approved', 'jalali_created']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__phone', 'post__title']
    readonly_fields = []
    actions = ['approve_comments', 'disapprove_comments']
    
    def jalali_created(self, obj):
        return format_date_for_admin(obj.created_at, include_time=True)
    jalali_created.short_description = 'تاریخ ثبت'
    
    def approve_comments(self, request, queryset):
        """تایید گروهی کامنت‌های انتخاب شده"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} دیدگاه با موفقیت تایید شد.')
    approve_comments.short_description = 'تایید دیدگاه‌های انتخاب شده'
    
    def disapprove_comments(self, request, queryset):
        """رد گروهی کامنت‌های انتخاب شده"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} دیدگاه رد شد.')
    disapprove_comments.short_description = 'رد دیدگاه‌های انتخاب شده'
