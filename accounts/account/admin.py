from django.contrib import admin

# Register your models here.
from .models import MasterPassword, Account

admin.site.register(Account)
admin.site.register(MasterPassword)
