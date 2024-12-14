from django.contrib.auth.models import BaseUserManager
from django.db import models
from decimal import Decimal



class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("user must be have mail")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class WalletManager(models.Manager):
    def create_wallet_for_user(self, user):
        return self.create(user=user, money=Decimal('0.00'))
    
    def add_money_to_wallet(self, user, amount):
        wallet, created = self.get_or_create(user=user)
        wallet.money += amount
        wallet.save()
        return wallet
    
    def pay_money_from_wallet(self, user, amount):
        wallet, created = self.get_or_create(user=user)
        if wallet.money >= amount:
            wallet.money -= amount
            wallet.save()
            return wallet
        else:
            raise ValueError("Insufficient balance")
    
    def get_current_money_by_user(self,user):
        wallet, created = self.get_or_create(user=user)
        return wallet.money

