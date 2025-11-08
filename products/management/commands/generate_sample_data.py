from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from PIL import Image
import random
import io

from products.models import Category, Product, ProductImage, ProductSpecification, Color, Brand
from blog.models import Post, Category as BlogCategory
from core.models import Banner, ContactInfo, FooterSettings, AdminSettings, About, AboutSection

User = get_user_model()

# Sample Persian texts
SAMPLE_TEXTS = [
    "این محصول با کیفیت بالا و طراحی مدرن تولید شده است. مناسب برای استفاده روزمره و دارای گارانتی معتبر می‌باشد.",
    "با خرید این محصول می‌توانید از مزایای بی‌نظیر آن بهره‌مند شوید. این محصول با آخرین تکنولوژی روز دنیا ساخته شده است.",
    "این محصول یکی از بهترین انتخاب‌ها در بازار است. دارای کیفیت عالی و قیمت مناسب می‌باشد.",
    "با استفاده از این محصول می‌توانید تجربه‌ای متفاوت داشته باشید. طراحی زیبا و عملکرد عالی از ویژگی‌های این محصول است.",
    "این محصول با توجه به نیازهای مشتریان طراحی شده است. دارای کیفیت بالا و دوام طولانی مدت می‌باشد.",
]


class Command(BaseCommand):
    help = 'پاک کردن تمام داده‌ها و ایجاد داده‌های نمونه'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='فقط داده‌ها را پاک کن (بدون ایجاد داده جدید)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_data()
            return

        self.stdout.write(self.style.WARNING('در حال پاک کردن تمام داده‌ها...'))
        self.clear_data()

        self.stdout.write(self.style.SUCCESS('در حال ایجاد داده‌های نمونه...'))
        
        # Create base settings
        self.create_base_settings()
        
        # Create colors
        colors = self.create_colors()
        
        # Create brands
        brands = self.create_brands()
        
        # Create product categories
        categories = self.create_product_categories()
        
        # Create products
        self.create_products(categories, colors, brands)
        
        # Create banners
        self.create_banners()
        
        # Create blog categories
        blog_categories = self.create_blog_categories()
        
        # Create blog posts
        self.create_blog_posts(blog_categories)
        
        # Create about page
        self.create_about_page()
        
        self.stdout.write(self.style.SUCCESS('✓ تمام داده‌های نمونه با موفقیت ایجاد شدند!'))

    def clear_data(self):
        """Clear all data"""
        ProductImage.objects.all().delete()
        ProductSpecification.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Color.objects.all().delete()
        Brand.objects.all().delete()
        
        Post.objects.all().delete()
        BlogCategory.objects.all().delete()
        
        Banner.objects.all().delete()
        
        AboutSection.objects.all().delete()
        About.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✓ تمام داده‌ها پاک شدند'))
    
    def create_base_settings(self):
        """Create base settings"""
        # AdminSettings
        AdminSettings.objects.get_or_create(
            id=1,
            defaults={
                'use_jalali_date': True,
                'site_title': 'دیجیتو',
                'site_header': 'پنل مدیریت دیجیتو',
                'site_index_title': 'خوش آمدید به پنل مدیریت',
                'show_hidden_models': False,
            }
        )
        
        # ContactInfo
        if not ContactInfo.objects.exists():
            ContactInfo.objects.create(
                phone='021-12345678',
                email='info@digito.ir',
                address='تهران، خیابان ولیعصر',
                working_hours='شنبه تا پنجشنبه: 9 صبح تا 6 عصر',
            )
        
        # FooterSettings
        if not FooterSettings.objects.exists():
            FooterSettings.objects.create(
                description='فروشگاه اینترنتی دیجیتو - بهترین محصولات دیجیتال',
                copyright_text='© 1403 تمام حقوق محفوظ است',
            )
        
        self.stdout.write(self.style.SUCCESS('✓ تنظیمات پایه ایجاد شد'))

    def create_colors(self):
        """Create colors"""
        colors_data = [
            ('قرمز', '#FF0000'),
            ('آبی', '#0000FF'),
            ('سبز', '#00FF00'),
            ('زرد', '#FFFF00'),
            ('مشکی', '#000000'),
            ('سفید', '#FFFFFF'),
            ('خاکستری', '#808080'),
            ('صورتی', '#FFC0CB'),
            ('بنفش', '#800080'),
            ('نارنجی', '#FFA500'),
        ]
        
        colors = []
        for name, hex_code in colors_data:
            color, created = Color.objects.get_or_create(
                name=name,
                defaults={'hex_code': hex_code}
            )
            colors.append(color)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {len(colors)} رنگ ایجاد شد'))
        return colors
    
    def create_brands(self):
        """Create brands"""
        brands_data = [
            ('سامسونگ', 1),
            ('اپل', 2),
            ('شیائومی', 3),
            ('هواوی', 4),
            ('سونی', 5),
            ('ال جی', 6),
            ('ایسوس', 7),
            ('لنوو', 8),
            ('نایک', 9),
            ('آدیداس', 10),
            ('پوما', 11),
            ('کانن', 12),
        ]
        
        brands = []
        for name, order in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=name,
                defaults={
                    'order': order,
                    'is_active': True,
                }
            )
            
            # Create simple logo for brand
            if created:
                logo_image = self.create_simple_image(200, 200, name)
                brand.logo.save(f'{name}_logo.png', ContentFile(logo_image), save=True)
            
            brands.append(brand)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {len(brands)} برند ایجاد شد'))
        return brands
    
    def create_simple_image(self, width, height, text=''):
        """Create simple image with text"""
        img = Image.new('RGB', (width, height), color=(240, 240, 240))
        
        # If PIL with text support is installed, text can be added
        # Otherwise, only a simple colored image is created
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
    
    def create_product_image(self, width=800, height=800):
        """Create product image"""
        # Create image with random color
        r = random.randint(200, 255)
        g = random.randint(200, 255)
        b = random.randint(200, 255)
        
        img = Image.new('RGB', (width, height), color=(r, g, b))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        return buffer.getvalue()
    
    def create_banner_image(self, width, height, banner_type='hero'):
        """Create banner image"""
        # Different colors for different banner types
        if banner_type == 'hero':
            color = (70, 130, 180)  # Steel blue
        elif banner_type == 'sidebar':
            color = (255, 140, 0)  # Orange
        else:
            color = (50, 205, 50)  # Green
        
        img = Image.new('RGB', (width, height), color=color)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=90)
        return buffer.getvalue()
    
    def create_blog_image(self, width=1200, height=600):
        """Create blog image"""
        # Soft colors for blog
        r = random.randint(180, 220)
        g = random.randint(180, 220)
        b = random.randint(180, 220)
        
        img = Image.new('RGB', (width, height), color=(r, g, b))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        return buffer.getvalue()

    def create_product_categories(self):
        """Create product categories with tree structure"""
        categories_data = {
            'الکترونیک': {
                'موبایل': ['گوشی هوشمند', 'گوشی معمولی', 'لوازم جانبی موبایل'],
                'لپ تاپ': ['لپ تاپ گیمینگ', 'لپ تاپ اداری', 'لپ تاپ دانشجویی'],
                'تبلت': ['تبلت 10 اینچ', 'تبلت 7 اینچ', 'تبلت 12 اینچ'],
            },
            'پوشاک': {
                'مردانه': ['تیشرت', 'شلوار', 'کت'],
                'زنانه': ['لباس', 'دامن', 'کفش'],
                'بچه گانه': ['لباس نوزاد', 'لباس کودک', 'کفش کودک'],
            },
            'خانه و آشپزخانه': {
                'مبلمان': ['مبل', 'صندلی', 'میز'],
                'لوازم آشپزخانه': ['قابلمه', 'ظروف', 'چاقو'],
                'دکوراسیون': ['تابلو', 'گلدان', 'آینه'],
            },
            'ورزش و سفر': {
                'ورزشی': ['کفش ورزشی', 'لباس ورزشی', 'توپ'],
                'سفر': ['چمدان', 'کوله پشتی', 'کیف مسافرتی'],
            },
        }
        
        categories = {}
        
        # Create main categories
        for main_name in categories_data.keys():
            main_cat, _ = Category.objects.get_or_create(
                name=main_name,
                defaults={'parent': None}
            )
            categories[main_name] = {'obj': main_cat, 'children': {}}
            
            # Create subcategories
            for sub_name, sub_children in categories_data[main_name].items():
                sub_cat, _ = Category.objects.get_or_create(
                    name=sub_name,
                    defaults={'parent': main_cat}
                )
                categories[main_name]['children'][sub_name] = {'obj': sub_cat, 'children': []}
                
                # Create third-level categories
                for child_name in sub_children:
                    child_cat, _ = Category.objects.get_or_create(
                        name=child_name,
                        defaults={'parent': sub_cat}
                    )
                    categories[main_name]['children'][sub_name]['children'].append(child_cat)
        
        # Rebuild MPTT tree
        Category.objects.rebuild()
        
        total = Category.objects.count()
        self.stdout.write(self.style.SUCCESS(f'✓ {total} دسته‌بندی محصول ایجاد شد'))
        return categories

    def create_products(self, categories, colors, brands):
        """Create products"""
        product_titles = [
            'گوشی موبایل سامسونگ گلکسی S24',
            'لپ تاپ ایسوس ROG Strix',
            'تبلت اپل iPad Pro',
            'تیشرت مردانه پنبه‌ای',
            'شلوار جین مردانه',
            'لباس زنانه تابستانی',
            'کفش زنانه کتانی',
            'مبل راحتی 3 نفره',
            'صندلی اداری ارگونومیک',
            'قابلمه استیل 5 لیتری',
            'چاقو آشپزخانه حرفه‌ای',
            'تابلو نقاشی مدرن',
            'گلدان سفالی بزرگ',
            'کفش ورزشی نایک',
            'چمدان مسافرتی 28 اینچ',
            'کوله پشتی کوهنوردی',
            'هدفون بی‌سیم سونی',
            'موس گیمینگ رزر',
            'کیبورد مکانیکی',
            'مانیتور 27 اینچ 4K',
            'اسپیکر بلوتوثی',
            'دوربین عکاسی کانن',
            'ساعت هوشمند اپل',
            'پاوربانک 20000 میلی‌آمپر',
            'فلش مموری 128 گیگابایت',
        ]
        
        products = []
        all_categories = []
        
        # Collect all categories
        for main_cat in categories.values():
            all_categories.append(main_cat['obj'])
            for sub_cat in main_cat['children'].values():
                all_categories.append(sub_cat['obj'])
                for child_cat in sub_cat['children']:
                    all_categories.append(child_cat)
        
        for i, title in enumerate(product_titles):
            # Select random category
            category = random.choice(all_categories)
            
            # Select random brand (70% chance of having a brand)
            brand = random.choice(brands) if random.random() < 0.7 and brands else None
            
            # Create product
            product = Product.objects.create(
                title=title,
                english_title=f"Product {i+1}",
                description=random.choice(SAMPLE_TEXTS) * 3,
                category=category,
                brand=brand,
                price=random.randint(50000, 50000000),
                stock=random.randint(0, 100),
                is_amazing=random.choice([True, False]),
                sales=random.randint(0, 1000),
                views=random.randint(0, 5000),
                warranty_months=random.choice([12, 18, 24, 36]),
                satisfaction_percent=random.randint(85, 100),
                delivery_date=random.randint(1, 7),
            )
            
            # Add random colors
            selected_colors = random.sample(colors, random.randint(1, min(3, len(colors))))
            product.colors.set(selected_colors)
            
            # Create product images (2-4 images)
            num_images = random.randint(2, 4)
            for img_num in range(num_images):
                image_data = self.create_product_image()
                product_image = ProductImage.objects.create(
                    product=product,
                    alt=f'{title} - تصویر {img_num + 1}'
                )
                product_image.image.save(
                    f'product_{product.id}_img_{img_num + 1}.jpg',
                    ContentFile(image_data),
                    save=True
                )
            
            # Create product specifications
            specs = [
                ('وزن', f'{random.randint(100, 5000)} گرم'),
                ('ابعاد', f'{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(5, 50)} سانتی‌متر'),
                ('جنس', random.choice(['پلاستیک', 'فلز', 'چوب', 'پارچه', 'شیشه'])),
                ('رنگ', ', '.join([c.name for c in selected_colors])),
            ]
            
            if brand:
                specs.append(('برند', brand.name))
            
            for key, value in specs:
                ProductSpecification.objects.create(
                    product=product,
                    key=key,
                    value=value
                )
            
            products.append(product)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {len(products)} محصول ایجاد شد'))
        return products

    def create_blog_categories(self):
        """Create blog categories"""
        from django.utils.text import slugify
        
        categories_data = [
            'فناوری',
            'سبک زندگی',
            'آموزش',
            'اخبار',
            'نقد و بررسی',
            'راهنما',
        ]
        
        categories = []
        for name in categories_data:
            slug = slugify(name)
            cat, _ = BlogCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
            categories.append(cat)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {len(categories)} دسته‌بندی بلاگ ایجاد شد'))
        return categories

    def create_blog_posts(self, categories):
        """Create blog posts"""
        post_titles = [
            'راهنمای خرید گوشی موبایل در سال 1403',
            'بهترین لپ تاپ‌های گیمینگ 2024',
            'نکات مهم در خرید مبلمان منزل',
            'راهنمای انتخاب کفش ورزشی مناسب',
            '10 نکته برای دکوراسیون خانه',
            'بهترین برندهای پوشاک ایرانی',
            'راهنمای نگهداری از لوازم آشپزخانه',
            'نقد و بررسی گوشی سامسونگ گلکسی S24',
            'مقایسه تبلت‌های اپل و سامسونگ',
            'راهنمای خرید لپ تاپ برای دانشجویان',
            'بهترین کفش‌های ورزشی برای دویدن',
            'نکات مهم در خرید چمدان مسافرتی',
            'راهنمای انتخاب هدفون مناسب',
            'بهترین مانیتورهای گیمینگ 2024',
            'راهنمای خرید دوربین عکاسی',
        ]
        
        # Get or create a user for author
        user, _ = User.objects.get_or_create(
            phone='09123456789',
            defaults={
                'fullname': 'مدیر سیستم',
            }
        )
        
        from django.utils.text import slugify
        
        posts = []
        for i, title in enumerate(post_titles):
            # Create unique slug
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            post = Post.objects.create(
                title=title,
                slug=slug,
                content=random.choice(SAMPLE_TEXTS) * 10,
                excerpt=random.choice(SAMPLE_TEXTS),
                author=user,
                category=random.choice(categories) if categories else None,
                status='published',
                views=random.randint(0, 1000),
                published_at=timezone.now(),
            )
            
            # Create image for blog post
            image_data = self.create_blog_image()
            post.image.save(
                f'blog_{post.id}.jpg',
                ContentFile(image_data),
                save=True
            )
            
            posts.append(post)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {len(posts)} پست بلاگ ایجاد شد'))
        return posts
    
    def create_banners(self):
        """Create banners"""
        # Hero banners
        hero_titles = [
            'فروش ویژه محصولات دیجیتال',
            'جدیدترین محصولات با بهترین قیمت',
            'تخفیف‌های شگفت‌انگیز',
        ]
        
        for i, title in enumerate(hero_titles):
            banner_image = self.create_banner_image(1920, 384, 'hero')
            banner = Banner.objects.create(
                title=title,
                banner_type='hero',
                order=i + 1,
                is_active=True,
                link='#',
            )
            banner.image.save(
                f'hero_banner_{i + 1}.jpg',
                ContentFile(banner_image),
                save=True
            )
        
        # Sidebar banner
        sidebar_image = self.create_banner_image(300, 600, 'sidebar')
        sidebar_banner = Banner.objects.create(
            title='محصولات جدید',
            banner_type='sidebar',
            order=1,
            is_active=True,
            link='#',
        )
        sidebar_banner.image.save(
            'sidebar_banner.jpg',
            ContentFile(sidebar_image),
            save=True
        )
        
        # Bottom banners
        bottom_titles = [
            'ارسال رایگان برای خرید بالای 500 هزار تومان',
            'گارانتی 18 ماهه برای تمام محصولات',
        ]
        
        for i, title in enumerate(bottom_titles):
            bottom_image = self.create_banner_image(1200, 675, 'bottom')
            banner = Banner.objects.create(
                title=title,
                banner_type='bottom',
                order=i + 1,
                is_active=True,
                link='#',
            )
            banner.image.save(
                f'bottom_banner_{i + 1}.jpg',
                ContentFile(bottom_image),
                save=True
            )
        
        self.stdout.write(self.style.SUCCESS('✓ بنرها ایجاد شدند'))
    
    def create_about_page(self):
        """Create about page"""
        # Create main about page
        about_content = """
        <h2>درباره دیجیتو</h2>
        <p>فروشگاه اینترنتی دیجیتو در سال 1400 با هدف ارائه بهترین محصولات دیجیتال به مشتریان عزیز تاسیس شد. ما با بیش از 3 سال تجربه در زمینه فروش آنلاین، همواره تلاش کرده‌ایم تا رضایت مشتریان را در اولویت اول قرار دهیم.</p>
        
        <h3>چرا دیجیتو؟</h3>
        <ul>
            <li>ارائه محصولات با کیفیت و اصل</li>
            <li>گارانتی معتبر و خدمات پس از فروش</li>
            <li>ارسال سریع و رایگان</li>
            <li>پشتیبانی 24 ساعته</li>
            <li>قیمت‌های رقابتی</li>
        </ul>
        
        <h3>ماموریت ما</h3>
        <p>ماموریت ما ارائه بهترین تجربه خرید آنلاین به مشتریان است. ما معتقدیم که هر مشتری حق دارد به محصولات با کیفیت و خدمات عالی دسترسی داشته باشد.</p>
        
        <h3>ارزش‌های ما</h3>
        <p>صداقت، کیفیت، رضایت مشتری و نوآوری از ارزش‌های اصلی ما هستند. ما همواره تلاش می‌کنیم تا این ارزش‌ها را در تمامی تعاملات خود با مشتریان حفظ کنیم.</p>
        """
        
        about_image = self.create_blog_image(1200, 800)
        about, created = About.objects.get_or_create(
            id=1,
            defaults={
                'title': 'درباره دیجیتو',
                'content': about_content,
                'is_active': True,
            }
        )
        
        if created:
            about.image.save(
                'about_main.jpg',
                ContentFile(about_image),
                save=True
            )
        
        # Create about sections
        about_sections = [
            {
                'title': 'تاریخچه ما',
                'content': 'دیجیتو در سال 1400 با یک تیم کوچک و پرانرژی شروع به کار کرد. در طول این سال‌ها، ما توانسته‌ایم به یکی از معتبرترین فروشگاه‌های آنلاین محصولات دیجیتال تبدیل شویم.',
                'order': 1,
            },
            {
                'title': 'تیم ما',
                'content': 'تیم دیجیتو متشکل از متخصصان با تجربه در زمینه‌های مختلف است. ما همواره تلاش می‌کنیم تا با به‌روزترین تکنولوژی‌ها و روش‌های کاری، بهترین خدمات را به مشتریان ارائه دهیم.',
                'order': 2,
            },
            {
                'title': 'دستاوردهای ما',
                'content': 'در طول این سال‌ها، ما موفق شده‌ایم به بیش از 50,000 مشتری راضی خدمات ارائه دهیم. رضایت مشتریان و اعتماد آنها به ما، بزرگترین دستاورد ما محسوب می‌شود.',
                'order': 3,
            },
            {
                'title': 'آینده ما',
                'content': 'ما در آینده قصد داریم تا دامنه محصولات خود را گسترش دهیم و خدمات بهتری به مشتریان ارائه کنیم. هدف ما تبدیل شدن به برترین فروشگاه آنلاین محصولات دیجیتال در ایران است.',
                'order': 4,
            },
        ]
        
        for section_data in about_sections:
            section = AboutSection.objects.create(
                about=about,
                title=section_data['title'],
                content=section_data['content'],
                order=section_data['order'],
            )
        
        self.stdout.write(self.style.SUCCESS('✓ صفحه درباره ما ایجاد شد'))

