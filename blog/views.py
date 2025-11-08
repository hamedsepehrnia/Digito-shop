from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post, Category, Comment
from .forms import CommentForm


def blog(request):
    """لیست پست‌های بلاگ"""
    posts = Post.objects.filter(status='published')
    
    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # صفحه‌بندی
    paginator = Paginator(posts, 9)  # 9 پست در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    blog_categories = Category.objects.all()
    
    context = {
        'posts': page_obj,
        'blog_categories': blog_categories,
        'selected_category': category_slug,
        'search_query': search_query,
    }
    
    return render(request, 'blog/blog.html', context)


def blog_detail(request, pk):
    """جزئیات یک پست بلاگ"""
    post = get_object_or_404(Post, pk=pk, status='published')
    
    # پست‌های مرتبط (از همان دسته‌بندی)
    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(pk=post.pk)[:3]
    
    # نظرات تایید شده
    comments = post.comments.filter(is_approved=True)
    
    # فرم نظر
    comment_form = CommentForm()
    
    # ثبت نظر جدید
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'برای ثبت دیدگاه باید وارد شوید.')
            return redirect('blog_detail', pk=post.pk)
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            try:
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.is_approved = False  # نیاز به تایید ادمین
                comment.save()
                messages.success(request, 'دیدگاه شما با موفقیت ثبت شد و پس از تایید نمایش داده خواهد شد.')
                return redirect('blog_detail', pk=post.pk)
            except Exception as e:
                messages.error(request, f'خطا در ثبت دیدگاه: {str(e)}')
        else:
            # نمایش خطاهای فرم
            error_messages = []
            for field, errors in comment_form.errors.items():
                for error in errors:
                    error_messages.append(f'{field}: {error}')
            messages.error(request, f'خطا در ثبت دیدگاه: {" ".join(error_messages)}')
    
    # افزایش تعداد بازدید (فقط برای GET request)
    if request.method == 'GET':
        post.views += 1
        post.save(update_fields=['views'])
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'blog/blogSingle.html', context)
