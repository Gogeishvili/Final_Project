from django.db import models
from decimal import Decimal

class WalletManager(models.Manager):
    def create_wallet_for_user(self, user):
        return self.create(user=user, money=Decimal("0.00"))

    def add_money_to_wallet_by_user(self, user, amount):
        wallet, created = self.get_or_create(user=user)
        wallet.money += amount
        wallet.save()
        return wallet

    def pay_money_from_wallet_by_user(self, user, amount):
        wallet, created = self.get_or_create(user=user)
        wallet.money -= amount
        wallet.save()
        return wallet

    def get_current_money_by_user(self, user):
        wallet, created = self.get_or_create(user=user)
        return wallet.money