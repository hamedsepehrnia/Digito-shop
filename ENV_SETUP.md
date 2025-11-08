# راهنمای تنظیم فایل .env

این فایل شامل راهنمای تنظیم متغیرهای محیطی برای پروژه دیجیتو است.

## نصب و راه‌اندازی

1. فایل `.env.example` را کپی کرده و نام آن را به `.env` تغییر دهید:
```bash
cp .env.example .env
```

2. فایل `.env` را باز کرده و مقادیر را با اطلاعات واقعی خود پر کنید.

## متغیرهای محیطی

### تنظیمات Django

- `DEBUG`: حالت دیباگ (True/False)
- `SECRET_KEY`: کلید مخفی Django
- `ALLOWED_HOSTS`: لیست هاست‌های مجاز (با کاما جدا شوند)

### تنظیمات پنل ادمین

- `ADMIN_SITE_TITLE`: عنوان سایت در تب مرورگر
- `ADMIN_SITE_HEADER`: هدر پنل ادمین
- `ADMIN_SITE_INDEX_TITLE`: عنوان صفحه اصلی پنل ادمین

### تنظیمات OTP (کاوه نگار)

- `KAVENEGAR_API_KEY`: کلید API کاوه نگار
- `KAVENEGAR_SENDER`: شماره فرستنده پیامک (پیش‌فرض: 10001001001)
- `OTP_USE_KAVENEGAR`: استفاده از کاوه نگار برای ارسال OTP (True/False)
  - اگر `False` و `DEBUG=True`: OTP در پیام نمایش داده می‌شود
  - اگر `True`: OTP از طریق کاوه نگار ارسال می‌شود
- `OTP_MAX_REQUESTS_PER_HOUR`: حداکثر تعداد درخواست OTP در هر ساعت (پیش‌فرض: 5)
- `OTP_MAX_REQUESTS_PER_DAY`: حداکثر تعداد درخواست OTP در هر روز (پیش‌فرض: 10)
- `OTP_EXPIRY_MINUTES`: مدت اعتبار OTP به دقیقه (پیش‌فرض: 5)

### تنظیمات پرداخت (زرین‌پال)

- `ZARINPAL_MERCHANT_ID`: شناسه مرچنت زرین‌پال
- `ZARINPAL_SANDBOX`: استفاده از محیط تست (True/False)
- `ZARINPAL_ACTIVE`: فعال کردن پرداخت زرین‌پال (True/False)
  - اگر `False`: پرداخت به صورت خودکار تایید می‌شود (برای تست)
  - اگر `True`: پرداخت از طریق زرین‌پال انجام می‌شود

## مثال فایل .env

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Admin Panel Settings
ADMIN_SITE_TITLE=دیجیتو
ADMIN_SITE_HEADER=پنل مدیریت دیجیتو
ADMIN_SITE_INDEX_TITLE=خوش آمدید به پنل مدیریت

# OTP Settings (Kavenegar)
KAVENEGAR_API_KEY=your-kavenegar-api-key-here
KAVENEGAR_SENDER=10001001001
OTP_USE_KAVENEGAR=False

# OTP Rate Limiting
OTP_MAX_REQUESTS_PER_HOUR=5
OTP_MAX_REQUESTS_PER_DAY=10
OTP_EXPIRY_MINUTES=5

# Payment Gateway (Zarinpal)
ZARINPAL_MERCHANT_ID=your-zarinpal-merchant-id-here
ZARINPAL_SANDBOX=True
ZARINPAL_ACTIVE=False
```

## نکات مهم

1. **هرگز فایل `.env` را در Git commit نکنید!** این فایل حاوی اطلاعات حساس است.
2. فایل `.env.example` را به عنوان الگو در Git نگه دارید.
3. در محیط production، حتماً `DEBUG=False` تنظیم کنید.
4. برای دریافت API Key کاوه نگار، به [پنل کاوه نگار](https://panel.kavenegar.com/) مراجعه کنید.
5. برای دریافت Merchant ID زرین‌پال، به [پنل زرین‌پال](https://www.zarinpal.com/) مراجعه کنید.

