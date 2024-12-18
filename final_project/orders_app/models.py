from django.db import models
from users_app.models import CustomUser
from games_app.models import Game
from .managers import *

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="cart")
    games = models.ManyToManyField(Game, related_name="carts")

    objects=CustomCartManager()

    def __str__(self):
        return f"{self.user.username}'s Cart"
    

class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="purchases")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="purchases")

    def __str__(self):
        return f"{self.user.username} purchased {self.game.name} on {self.purchased_at}"
