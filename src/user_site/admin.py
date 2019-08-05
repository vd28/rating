from django.contrib import admin
from . import models


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('university', 'revision', 'active')
    list_editable = ('active',)
    list_select_related = ('revision', 'university')
    ordering = ('-revision__created_at', 'university__name')
    autocomplete_fields = ('university',)

    def save_model(self, request, obj, form, change):
        models.Config.objects.select_for_update().filter(active=True).update(active=False)
        super().save_model(request, obj, form, change)
