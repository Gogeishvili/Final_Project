from django.db import models


class Book:

    def __init__(self, name, price):
        self.name = name
        self.price = price
