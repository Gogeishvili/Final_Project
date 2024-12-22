from django.db.models.signals import post_save
from django.dispatch import receiver
from users_app.models import CustomUser
from .models import *


@receiver(post_save, sender=CustomUser)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
