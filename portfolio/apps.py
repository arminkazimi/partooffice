from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "portfolio"

    def ready(self):
        from django.contrib import admin
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group

        User = get_user_model()
        for model in (User, Group):
            try:
                admin.site.unregister(model)
            except admin.sites.NotRegistered:
                pass
