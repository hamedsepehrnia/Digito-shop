from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.urls import path
from django.contrib import messages
from products.models import Product, Category, Brand
from blog.models import Post
from accounts.models import Favorite
from .models import About, AboutSection, ContactInfo, Banner
from .forms import ContactMessageForm

class HomePageView(TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Best-selling products (based on sales)
        context['bestseller_products'] = Product.objects.order_by('-sales')[:10]
        # Amazing products
        context['amazing_products'] = Product.objects.filter(is_amazing=True)[:10]
        # Latest products
        context['latest_products'] = Product.objects.order_by('-created_at')[:10]
        # Latest blog posts
        context['latest_posts'] = Post.objects.filter(status='published').order_by('-created_at')[:6]
        # Categories - using context processor, no need to override
        # If you need to limit, you can use context['categories'][:7] in template
        
        # Hero banners (Hero Slider)
        context['hero_banners'] = Banner.objects.filter(banner_type='hero', is_active=True).order_by('order', 'id')
        # Bottom banners
        context['bottom_banners'] = Banner.objects.filter(banner_type='bottom', is_active=True).order_by('order', 'id')[:2]
        # Sidebar banner (for display next to amazing products)
        context['sidebar_banner'] = Banner.objects.filter(banner_type='sidebar', is_active=True).order_by('order', 'id').first()
        
        # Brands (for display in brands section)
        context['brands'] = Brand.objects.filter(is_active=True).order_by('order', 'name')
        
        # Check favorites for logged-in users
        user_favorites = set()
        if self.request.user.is_authenticated:
            user_favorites = set(Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True))
        context['user_favorites'] = user_favorites
        
        return context

class AboutPageView(TemplateView):
    template_name = 'core/aboutUs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get about us content (first active record)
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
    """Contact us page"""
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
            # Display form errors
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
