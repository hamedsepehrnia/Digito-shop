from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'content', 'created_at', 'is_approved']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'jalali_created', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at', 'published_at']
    inlines = [CommentInline]
    actions = ['publish_posts', 'draft_posts']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('محتوا', {
            'fields': ('excerpt', 'content', 'image')
        }),
        ('آمار', {
            'fields': ('views', 'created_at', 'updated_at', 'published_at')
        }),
    )
    
    def jalali_created(self, obj):
        return obj.jalali_created()
    jalali_created.short_description = 'تاریخ ایجاد (شمسی)'
    
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_approved', 'jalali_created', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__phone', 'post__title']
    readonly_fields = ['created_at']
    actions = ['approve_comments', 'disapprove_comments']
    
    def jalali_created(self, obj):
        return obj.jalali_created()
    jalali_created.short_description = 'تاریخ (شمسی)'
    
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
