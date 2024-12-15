from django.db import models
from users_app.models import CustomUser


class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    author = models.ForeignKey(CustomUser, related_name="game", on_delete=models.CASCADE)
