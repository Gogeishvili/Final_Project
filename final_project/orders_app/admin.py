from django.contrib import admin
from .models import *


@admin.register(Cart)
class WalletAdmin(admin.ModelAdmin):
    fields = ["user","games"]
