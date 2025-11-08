from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.urls import path
from django.contrib import messages
from products.models import Product, Category
from blog.models import Post
from accounts.models import Favorite
from .models import About, AboutSection, ContactInfo
from .forms import ContactMessageForm

class HomePageView(TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # پرفروش‌ترین محصولات (بر اساس sales)
        context['bestseller_products'] = Product.objects.order_by('-sales')[:10]
        # محصولات شگفت‌انگیز
        context['amazing_products'] = Product.objects.filter(is_amazing=True)[:10]
        # جدیدترین محصولات
        context['latest_products'] = Product.objects.order_by('-created_at')[:10]
        # جدیدترین پست‌های بلاگ
        context['latest_posts'] = Post.objects.filter(status='published').order_by('-created_at')[:6]
        # دسته‌بندی‌ها - از context processor استفاده می‌شود، نیازی به override نیست
        # اگر نیاز به محدود کردن دارید، می‌توانید از context['categories'][:7] در template استفاده کنید
        
        # بررسی favorite برای کاربران لاگین شده
        user_favorites = set()
        if self.request.user.is_authenticated:
            user_favorites = set(Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True))
        context['user_favorites'] = user_favorites
        
        return context

class AboutPageView(TemplateView):
    template_name = 'core/aboutUs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # دریافت محتوای درباره ما (اولین رکورد فعال)
        about = About.objects.filter(is_active=True).first()
        if about:
            context['about'] = about
            context['sections'] = about.sections.all()
        return context

class RulesPageView(TemplateView):
    template_name = 'core/rules.html'

class FaqPageView(TemplateView):
    template_name = 'core/faq.html'

def contact_us(request):
    """صفحه تماس با ما"""
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    form = ContactMessageForm()
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'پیام شما با موفقیت ارسال شد. در اسرع وقت با شما تماس خواهیم گرفت.')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'خطا در ارسال پیام: {str(e)}')
        else:
            # نمایش خطاهای فرم
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'{field}: {error}')
            messages.error(request, f'خطا در ارسال پیام: {" ".join(error_messages)}')
    
    context = {
        'contact_info': contact_info,
        'form': form,
    }
    return render(request, 'core/contactUs.html', context)
