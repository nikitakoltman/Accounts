from django.contrib import admin

from .models import Account, MasterPassword, TokenConfirmEmail


class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'site', 'updated']

    class Meta:
        model = Account

class MasterPasswordAdmin(admin.ModelAdmin):
    list_display = ['user', 'password']

    class Meta:
        model = MasterPassword


admin.site.register(Account)
admin.site.register(MasterPassword)
admin.site.register(TokenConfirmEmail)