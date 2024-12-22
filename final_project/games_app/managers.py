from django.db import models


class GameManager(models.Manager):
    def get_games_by_author(self, author):
        return self.filter(author=author)

    def get_games_in_price_range(self, min_price, max_price):
        return self.filter(price__gte=min_price, price__lte=max_price)
