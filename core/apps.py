from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "تنظیمات اصلی"
    
    def ready(self):
        """Connect signal handler for updating hidden models"""
        from django.db.models.signals import post_save
        from core.models import AdminSettings
        from Digito.admin import update_hidden_models
        
        def refresh_hidden_models(sender, instance, **kwargs):
            """Update hidden models after saving AdminSettings"""
            if isinstance(instance, AdminSettings):
                update_hidden_models()
        
        post_save.connect(refresh_hidden_models, sender=AdminSettings)
