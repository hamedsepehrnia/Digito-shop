# Digito

A comprehensive and professional e-commerce platform built with Django for digital product sales.

[![Persian](https://img.shields.io/badge/lang-persian-blue?style=for-the-badge)](#فارسی)
[![English](https://img.shields.io/badge/lang-English-green?style=for-the-badge)](#english)

---

## Support

<a href="https://www.coffeebede.com/hamesep">
  <img src="https://coffeebede.ir/DashboardTemplateV2/app-assets/images/banner/default-yellow.svg" alt="Buy Me A Coffee" height="60">
</a>

<a href="https://nowpayments.io/donation?api_key=19623fa3-605a-436a-97cd-b5859356b41d" target="_blank">
  <img src="https://img.shields.io/badge/Donate-Crypto-blue?style=for-the-badge&logo=bitcoin&logoColor=white" alt="Donate with Crypto" height="50">
</a>

---

## English

### Overview

Digito is a full-featured e-commerce platform designed for selling digital products. Built with Django 5.2, it provides a complete solution for managing products, orders, user accounts, and content management with a Persian-first approach.

### Features

#### E-Commerce Core
- Multi-level hierarchical category system (MPTT) with mega menu
- Brand management with logo and filtering
- Advanced product filtering:
  - Filter by category
  - Filter by brand
  - Filter by color
  - Price range slider
  - Stock availability filter
- Advanced product search
- Product sorting (newest, best-selling, cheapest, most expensive, most viewed)
- Product pagination
- Featured products display
- Product image gallery
- Product reviews and rating system
- Technical specifications display

#### User Management
- Phone number authentication with OTP
- Complete user dashboard:
  - Order statistics
  - Wishlist management
  - Address management
  - Order history
- Advanced shopping cart
- Favorite products system
- Multiple address management
- Order tracking

#### Blog System
- Complete blog functionality
- Post categorization
- Comment system for posts
- Blog search

#### Content Management
- Dynamic banner management:
  - Hero slider banners
  - Sidebar banners
  - Bottom page banners
- About page management
- Contact information management
- Footer links management
- Social media management

#### Admin Panel
- Fully Persianized admin interface
- Vazir font for better Persian text display
- Automatic date conversion to Jalali (with option to switch to Gregorian)
- Image preview in lists
- Statistics and useful information display
- Advanced mode: show/hide less-used models
- Date settings: choose between Jalali and Gregorian calendars
- Singleton pattern for contact and footer settings

### Technology Stack

| Category | Technology |
|----------|-----------|
| **Backend Framework** | Django 5.2 |
| **Database** | SQLite (configurable to PostgreSQL/MySQL) |
| **Frontend** | HTML5, CSS3, Tailwind CSS, JavaScript |
| **Category System** | django-mptt 0.17.0+ |
| **Date/Time** | persiantools (Jalali calendar) |
| **Image Processing** | Pillow 10.0.0+ |
| **Slug Generation** | python-slugify 8.0.0+ (Persian/Unicode support) |
| **Environment Variables** | python-decouple 3.8+ |
| **Payment Gateway** | Zarinpal (via requests) |
| **Fake Data** | Faker 20.0.0+ |

### Installation

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd Digito
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Frontend: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

### Configuration

#### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Admin Settings
ADMIN_SITE_TITLE=دیجیتو
ADMIN_SITE_HEADER=پنل مدیریت دیجیتو
ADMIN_SITE_INDEX_TITLE=خوش آمدید به پنل مدیریت

# OTP Settings (Kavenegar)
KAVENEGAR_API_KEY=your-api-key
KAVENEGAR_SENDER=10001001001
OTP_USE_KAVENEGAR=False
OTP_MAX_REQUESTS_PER_HOUR=5
OTP_MAX_REQUESTS_PER_DAY=10
OTP_EXPIRY_MINUTES=5

# Payment Gateway (Zarinpal)
ZARINPAL_MERCHANT_ID=your-merchant-id
ZARINPAL_SANDBOX=True
ZARINPAL_ACTIVE=False
```

### Project Structure

```
Digito/
├── accounts/          # User management and authentication
├── blog/             # Blog system
├── cart/             # Shopping cart
├── core/             # Main pages and settings
├── orders/           # Order management
├── products/         # Product management
├── static/           # Static files (CSS, JS, Images)
├── templates/        # HTML templates
├── media/            # Uploaded files
└── contex_processors/ # Context processors
```

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

### License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** License.

This license allows you to:
- Share: Copy and redistribute the material in any medium or format
- Adapt: Remix, transform, and build upon the material

**Restrictions:**
- Commercial use is not permitted

For more details, see the [LICENSE](LICENSE) file or visit [Creative Commons](https://creativecommons.org/licenses/by-nc/4.0/).

### Support

- **Report Issues**: [GitHub Issues](https://github.com/[username]/Digito/issues)
- **Questions**: Open a discussion in the repository

---

## فارسی

### بررسی کلی

دیجیتو یک پلتفرم تجارت الکترونیک کامل و حرفه‌ای است که با Django 5.2 ساخته شده و برای فروش محصولات دیجیتال طراحی شده است. این پروژه راه‌حل کاملی برای مدیریت محصولات، سفارش‌ها، حساب‌های کاربری و مدیریت محتوا با رویکرد فارسی‌محور ارائه می‌دهد.

### ویژگی‌ها

#### هسته فروشگاه
- سیستم دسته‌بندی چندسطحی (MPTT) با منوی مگا
- مدیریت برندها با لوگو و فیلتر
- فیلتر پیشرفته محصولات:
  - فیلتر بر اساس دسته‌بندی
  - فیلتر بر اساس برند
  - فیلتر بر اساس رنگ
  - اسلایدر محدوده قیمت
  - فیلتر موجودی محصولات
- جستجوی پیشرفته در محصولات
- مرتب‌سازی محصولات (جدیدترین، پرفروش‌ترین، ارزان‌ترین، گران‌ترین، پربازدیدترین)
- صفحه‌بندی محصولات
- نمایش محصولات شگفت‌انگیز
- گالری تصاویر محصولات
- سیستم نظرات و امتیازدهی
- نمایش مشخصات فنی محصولات

#### مدیریت کاربران
- احراز هویت با شماره تلفن (OTP)
- داشبورد کاربری کامل:
  - آمار سفارش‌ها
  - مدیریت لیست علاقه‌مندی‌ها
  - مدیریت آدرس‌ها
  - تاریخچه سفارش‌ها
- سبد خرید پیشرفته
- سیستم علاقه‌مندی (Favorite)
- مدیریت چندین آدرس
- پیگیری سفارش‌ها

#### سیستم بلاگ
- عملکرد کامل بلاگ
- دسته‌بندی پست‌ها
- سیستم نظرات برای پست‌ها
- جستجو در بلاگ

#### مدیریت محتوا
- مدیریت بنرهای داینامیک:
  - بنرهای اسلایدر اصلی
  - بنرهای کناری
  - بنرهای پایین صفحه
- مدیریت صفحه درباره ما
- مدیریت اطلاعات تماس
- مدیریت لینک‌های فوتر
- مدیریت شبکه‌های اجتماعی

#### پنل مدیریت
- رابط کاربری کاملاً فارسی‌سازی شده
- فونت Vazir برای نمایش بهتر متن‌های فارسی
- تبدیل خودکار تاریخ به شمسی (با امکان تغییر به میلادی)
- پیش‌نمایش تصویر در لیست‌ها
- نمایش آمار و اطلاعات مفید
- حالت پیشرفته: نمایش/پنهان کردن مدل‌های کم‌استفاده
- تنظیمات تاریخ: انتخاب بین تقویم شمسی و میلادی
- الگوی Singleton برای تنظیمات تماس و فوتر

### تکنولوژی‌های استفاده شده

| دسته‌بندی | تکنولوژی |
|----------|----------|
| **فریمورک بک‌اند** | Django 5.2 |
| **پایگاه داده** | SQLite (قابل تغییر به PostgreSQL/MySQL) |
| **فرانت‌اند** | HTML5, CSS3, Tailwind CSS, JavaScript |
| **سیستم دسته‌بندی** | django-mptt 0.17.0+ |
| **تاریخ/زمان** | persiantools (تقویم شمسی) |
| **پردازش تصویر** | Pillow 10.0.0+ |
| **تولید Slug** | python-slugify 8.0.0+ (پشتیبانی فارسی/Unicode) |
| **متغیرهای محیطی** | python-decouple 3.8+ |
| **درگاه پرداخت** | زرین‌پال (از طریق requests) |
| **داده‌های تست** | Faker 20.0.0+ |

### نصب و راه‌اندازی

1. **کلون کردن ریپازیتوری**
   ```bash
   git clone [آدرس-ریپازیتوری]
   cd Digito
   ```

2. **ایجاد محیط مجازی (توصیه می‌شود)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # یا
   .venv\Scripts\activate  # Windows
   ```

3. **نصب وابستگی‌ها**
   ```bash
   pip install -r requirements.txt
   ```

4. **پیکربندی متغیرهای محیطی**
   ```bash
   cp .env.example .env
   # فایل .env را با تنظیمات خود ویرایش کنید
   ```

5. **اجرای Migration ها**
   ```bash
   python manage.py migrate
   ```

6. **ایجاد کاربر ادمین**
   ```bash
   python manage.py createsuperuser
   ```

7. **اجرای سرور توسعه**
   ```bash
   python manage.py runserver
   ```

8. **دسترسی به برنامه**
   - رابط کاربری: http://127.0.0.1:8000
   - پنل مدیریت: http://127.0.0.1:8000/admin

### پیکربندی

#### متغیرهای محیطی

یک فایل `.env` در ریشه پروژه ایجاد کنید و متغیرهای زیر را تنظیم کنید:

```env
SECRET_KEY=کلید-رمز-شما
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# تنظیمات ادمین
ADMIN_SITE_TITLE=دیجیتو
ADMIN_SITE_HEADER=پنل مدیریت دیجیتو
ADMIN_SITE_INDEX_TITLE=خوش آمدید به پنل مدیریت

# تنظیمات OTP (کاوه‌نگار)
KAVENEGAR_API_KEY=کلید-API-شما
KAVENEGAR_SENDER=10001001001
OTP_USE_KAVENEGAR=False
OTP_MAX_REQUESTS_PER_HOUR=5
OTP_MAX_REQUESTS_PER_DAY=10
OTP_EXPIRY_MINUTES=5

# درگاه پرداخت (زرین‌پال)
ZARINPAL_MERCHANT_ID=شناسه-فروشنده-شما
ZARINPAL_SANDBOX=True
ZARINPAL_ACTIVE=False
```

### ساختار پروژه

```
Digito/
├── accounts/          # مدیریت کاربران و احراز هویت
├── blog/             # سیستم بلاگ
├── cart/             # سبد خرید
├── core/             # صفحات اصلی و تنظیمات
├── orders/           # مدیریت سفارش‌ها
├── products/         # مدیریت محصولات
├── static/           # فایل‌های استاتیک (CSS, JS, Images)
├── templates/        # قالب‌های HTML
├── media/            # فایل‌های آپلود شده
└── contex_processors/ # پردازشگرهای Context
```

### مشارکت

مشارکت‌ها خوش‌آمد هستند! لطفاً این مراحل را دنبال کنید:

1. ریپازیتوری را Fork کنید
2. یک شاخه ویژگی ایجاد کنید (`git checkout -b feature/ویژگی-عالی`)
3. تغییرات خود را Commit کنید (`git commit -m 'افزودن ویژگی عالی'`)
4. به شاخه Push کنید (`git push origin feature/ویژگی-عالی`)
5. یک Pull Request باز کنید

لطفاً اطمینان حاصل کنید که کد شما از استانداردهای کدنویسی پروژه پیروی می‌کند و شامل تست‌های مناسب است.

### لایسنس

این پروژه تحت لایسنس **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** منتشر شده است.

این لایسنس به شما اجازه می‌دهد:
- اشتراک‌گذاری: کپی و توزیع مطالب در هر رسانه و فرمتی
- تغییر: ترکیب، تبدیل و ساخت بر اساس این مطالب

**محدودیت‌ها:**
- استفاده تجاری مجاز نیست

برای جزئیات بیشتر، فایل [LICENSE](LICENSE) را مطالعه کنید یا به [Creative Commons](https://creativecommons.org/licenses/by-nc/4.0/) مراجعه کنید.

### پشتیبانی

- **گزارش مشکل**: [GitHub Issues](https://github.com/[username]/Digito/issues)
- **سوالات**: یک Discussion در ریپازیتوری باز کنید

---

<div align="center">

*Version* 1.0.0 | *Django* 5.2 | *Python* 3.8+

<img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey?style=for-the-badge" alt="License">

---

© 2025 Digito

</div>

