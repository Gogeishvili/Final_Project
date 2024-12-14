from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class AuthorAdmin(admin.ModelAdmin):
    fields = ["email", "username", "password"]


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    fields = ["money", "user"]
