from django.contrib import admin

from users import models


@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass
