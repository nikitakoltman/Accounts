from django.contrib import admin

from .models import Account, MasterPassword

admin.site.register(Account)
admin.site.register(MasterPassword)
