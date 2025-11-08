from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
import random

from products.models import Category, Product, ProductImage, ProductSpecification, Color
from blog.models import Post, Category as BlogCategory

User = get_user_model()

# متن‌های نمونه فارسی
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
        
        # ایجاد رنگ‌ها
        colors = self.create_colors()
        
        # ایجاد دسته‌بندی‌های محصولات
        categories = self.create_product_categories()
        
        # ایجاد محصولات
        self.create_products(categories, colors)
        
        # ایجاد دسته‌بندی‌های بلاگ
        blog_categories = self.create_blog_categories()
        
        # ایجاد پست‌های بلاگ
        self.create_blog_posts(blog_categories)
        
        self.stdout.write(self.style.SUCCESS('✓ تمام داده‌های نمونه با موفقیت ایجاد شدند!'))

    def clear_data(self):
        """پاک کردن تمام داده‌ها"""
        ProductImage.objects.all().delete()
        ProductSpecification.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Color.objects.all().delete()
        
        Post.objects.all().delete()
        BlogCategory.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✓ تمام داده‌ها پاک شدند'))

    def create_colors(self):
        """ایجاد رنگ‌ها"""
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

    def create_product_categories(self):
        """ایجاد دسته‌بندی‌های محصولات با ساختار درختی"""
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
        
        # ایجاد دسته‌بندی‌های اصلی
        for main_name in categories_data.keys():
            main_cat, _ = Category.objects.get_or_create(
                name=main_name,
                defaults={'parent': None}
            )
            categories[main_name] = {'obj': main_cat, 'children': {}}
            
            # ایجاد دسته‌بندی‌های فرعی
            for sub_name, sub_children in categories_data[main_name].items():
                sub_cat, _ = Category.objects.get_or_create(
                    name=sub_name,
                    defaults={'parent': main_cat}
                )
                categories[main_name]['children'][sub_name] = {'obj': sub_cat, 'children': []}
                
                # ایجاد دسته‌بندی‌های سطح سوم
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

    def create_products(self, categories, colors):
        """ایجاد محصولات"""
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
        
        # جمع‌آوری تمام دسته‌بندی‌ها
        for main_cat in categories.values():
            all_categories.append(main_cat['obj'])
            for sub_cat in main_cat['children'].values():
                all_categories.append(sub_cat['obj'])
                for child_cat in sub_cat['children']:
                    all_categories.append(child_cat)
        
        for i, title in enumerate(product_titles):
            # انتخاب دسته‌بندی تصادفی
            category = random.choice(all_categories)
            
            # ایجاد محصول
            product = Product.objects.create(
                title=title,
                english_title=f"Product {i+1}",
                description=random.choice(SAMPLE_TEXTS) * 3,
                category=category,
                price=random.randint(50000, 50000000),
                stock=random.randint(0, 100),
                is_amazing=random.choice([True, False]),
                sales=random.randint(0, 1000),
                views=random.randint(0, 5000),
                warranty_months=random.choice([12, 18, 24, 36]),
                satisfaction_percent=random.randint(85, 100),
                delivery_date=random.randint(1, 7),
            )
            
            # افزودن رنگ‌های تصادفی
            selected_colors = random.sample(colors, random.randint(1, 3))
            product.colors.set(selected_colors)
            
            # ایجاد مشخصات محصول
            specs = [
                ('وزن', f'{random.randint(100, 5000)} گرم'),
                ('ابعاد', f'{random.randint(10, 100)}x{random.randint(10, 100)}x{random.randint(5, 50)} سانتی‌متر'),
                ('جنس', random.choice(['پلاستیک', 'فلز', 'چوب', 'پارچه', 'شیشه'])),
                ('رنگ', ', '.join([c.name for c in selected_colors])),
            ]
            
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
        """ایجاد دسته‌بندی‌های بلاگ"""
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
        """ایجاد پست‌های بلاگ"""
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
        
        # دریافت یا ایجاد یک کاربر برای نویسنده
        user, _ = User.objects.get_or_create(
            phone='09123456789',
            defaults={
                'fullname': 'مدیر سیستم',
            }
        )
        
        from django.utils.text import slugify
        
        posts = []
        for i, title in enumerate(post_titles):
            # ایجاد slug منحصر به فرد
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
            posts.append(post)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {len(posts)} پست بلاگ ایجاد شد'))
        return posts

