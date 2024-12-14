from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import *


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class Wallet(models.Model):
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='wallet')

    def __str__(self):
        return f"Wallet for {self.user} - Balance: {self.money} USD"
