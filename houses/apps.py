from django.apps import AppConfig


class HousesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'houses'

def ready(self):
        from . import admin
        self.admin_site = admin.MyAdminSite()