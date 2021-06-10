from django.contrib import admin
from authorization.models import ConfirmationEmail


@admin.register(ConfirmationEmail)
class ConfirmationEmailAdmin(admin.ModelAdmin):
    pass
