from django.contrib import admin

from tours_parser import models


@admin.register(models.ToursProviders)
class ToursProvidersAdmin(admin.ModelAdmin):
    pass
