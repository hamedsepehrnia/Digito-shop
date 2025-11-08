from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "تنظیمات اصلی"
    
    def ready(self):
        """اتصال signal handler برای به‌روزرسانی مدل‌های پنهان"""
        from django.db.models.signals import post_save
        from core.models import AdminSettings
        from Digito.admin import update_hidden_models
        
        def refresh_hidden_models(sender, instance, **kwargs):
            """به‌روزرسانی مدل‌های پنهان پس از ذخیره AdminSettings"""
            if isinstance(instance, AdminSettings):
                update_hidden_models()
        
        post_save.connect(refresh_hidden_models, sender=AdminSettings)
