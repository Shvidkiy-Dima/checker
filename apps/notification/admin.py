from django.contrib import admin
from notification.models import TelegramConfirmation

@admin.register(TelegramConfirmation)
class TelegramConfirmationAdmin(admin.ModelAdmin):
    pass