from django.contrib import admin
from .models import *


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    fields = ["money", "user"]
