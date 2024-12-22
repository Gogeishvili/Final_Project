from celery import shared_task
from orders_app.models import Cart
from games_app.models import Game

@shared_task
def add_game_to_cart(user_id, game_id):
    from django.contrib.auth import get_user_model
    CustomUser = get_user_model()

    user = CustomUser.objects.get(id=user_id)
    game = Game.objects.get(id=game_id)
    cart, _ = Cart.objects.get_or_create(user=user)
    cart.games.add(game)
    return f"Game {game.name} added to {user.username}'s cart."
