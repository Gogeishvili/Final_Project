from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=CustomUser)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create_wallet_for_user(user=instance)