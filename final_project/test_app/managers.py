from django.db import models


class BookManager(models.Manager):
    def get_total_price(self, book_id):
        book = self.get(id=book_id)
        return book.price * book.quantity
    

