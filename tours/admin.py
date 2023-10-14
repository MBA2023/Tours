from django.contrib import admin

from tours import models


class TourImageInline(admin.TabularInline):
    model = models.TourImage


@admin.register(models.Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [
        TourImageInline,
    ]


@admin.register(models.Guide)
class GuideAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass
