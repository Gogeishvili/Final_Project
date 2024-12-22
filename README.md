# Django Gaming Platform

This project is a Django-based gaming platform where users can manage wallets, purchase games, and maintain carts. The application is divided into four main apps: `user_app`, `wallet_app`, `order_app`, and `games_app`.

## Project Structure
├── user_app │ ├── models.py │ ├── serializers.py │ └── views.py │ ├── wallet_app │ ├── models.py │ └── views.py │ ├── order_app │ ├── models.py │ └── views.py │ ├── games_app │ ├── models.py │ └── views.py │ └── README.md

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/django-gaming-platform.git
cd django-gaming-platform

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

Endpoints
Authentication
POST /api/token/ - Obtain access and refresh tokens
POST /api/token/refresh/ - Refresh access token
User Management (user_app)
GET /users/ - List users
POST /users/ - Register user
GET /users/<username>/ - Retrieve user details
DELETE /users/<username>/ - Delete user
Wallet Management (wallet_app)
GET /wallet/ - List wallets
POST /wallet/add_money/ - Add money to wallet
POST /wallet/pay_money/ - Deduct money from wallet
Cart and Purchase (order_app)
GET /carts/ - List carts
GET /carts/<id>/purchase/ - Purchase games in the cart
GET /purchase/ - List purchases
GET /purchase/most_sold_games/ - List most sold games
Game Management (games_app)
GET /games/ - List games
POST /games/ - Add a new game
GET /games/<name>/ - Retrieve game details
GET /games/<name>/add_game_cart/ - Add game to cart
Models Overview
user_app.models.CustomUser
username - User's unique identifier
email - User's email
is_active - Status of user
is_staff - Admin privileges
is_superuser - Superuser privileges
wallet_app.models.Wallet
money - Balance in wallet
user - Associated user
order_app.models.Cart
user - Associated user
games - Games in cart
order_app.models.Purchase
user - Buyer
game - Purchased game
games_app.models.Game
name - Game title
price - Game price
author - Creator of game

python manage.py test
