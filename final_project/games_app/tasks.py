from celery import shared_task
from orders_app.models import Cart, Game
from users_app.models import CustomUser

@shared_task
def add_game_to_cart(user_id, game_id):
    user = CustomUser.objects.get(id=user_id)
    game = Game.objects.get(id=game_id)
    
    try:
        cart = Cart.objects.add_game_in_cart(user, game)
        return f"Game {game.name} added to {user.username}'s cart."
    except ValueError as e:
        return str(e)