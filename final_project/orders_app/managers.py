from django.contrib.auth.models import BaseUserManager
from django.db import models
from decimal import Decimal


class CustomCartManager(BaseUserManager):

    def add_game_in_cart(self, user, game, **extra_fields):
        try:
            cart = user.cart
        except cart.DoesNotExist:
            cart = self.create(user=user)

        if cart.games.filter(id=game.id).exists():
            raise ValueError(f"The game '{game.name}' is already in your cart.")

        cart.games.add(game)
        return cart

    
    