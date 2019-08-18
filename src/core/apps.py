from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = _('Application Management')

    def ready(self):
        from django.contrib import admin
        admin.site.site_header = 'Rating admin'
