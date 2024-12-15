from django.contrib import admin
from .models import *


@admin.register(Game)
class WalletAdmin(admin.ModelAdmin):
    fields = ["name", "price","author"]
