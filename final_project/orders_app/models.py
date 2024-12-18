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
    


