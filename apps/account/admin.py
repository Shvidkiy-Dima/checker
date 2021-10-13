from django.contrib import admin
from account.models import ClientAlert, User, ClientProfile
from configs.models import UserConfig


class ClientProfileTabularInline(admin.TabularInline):
    model = ClientProfile
    extra = 0


class UserConfigTabularInline(admin.TabularInline):
    model = UserConfig
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [ClientProfileTabularInline, UserConfigTabularInline]


@admin.register(ClientAlert)
class ClientAlertAdmin(admin.ModelAdmin):
    pass
