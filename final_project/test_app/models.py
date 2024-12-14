from django.db import models
from .managers import *


class Book:

    def __init__(self, name, price):
        self.name = name
        self.price = price


class BookModel(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    objects = BookManager()

    def __str__(self):
        return self.name
