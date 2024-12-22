from django.db import models
from users_app.models import CustomUser
from .managers import WalletManager


class Wallet(models.Model):
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="wallet"
    )

    objects = WalletManager()

    def __str__(self):
        return f"Wallet for {self.user} - Balance: {self.money} USD"
