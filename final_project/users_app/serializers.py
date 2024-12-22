from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from helpers import validate_string_match, validate_password_strength
from games_app.models import Game
from orders_app.models import Cart, Purchase
from wallet_app.models import Wallet
from .models import *


class WalletNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["money"]


class GameNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["name", "price"]


class CartNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class PurchiseNestedSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(source="game.name", read_only=True)

    class Meta:
        model = Purchase
        fields = ["id", "game_name"]


class UserSerializer(serializers.ModelSerializer):
    wallet = WalletNestedSerializer(many=True, read_only=True)
    games = GameNestedSerializer(many=True, read_only=True)
    cart = CartNestedSerializer(many=False, read_only=True)
    purchases = PurchiseNestedSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "wallet", "games", "cart", "purchases"]


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True, required=True, label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        validate_string_match(password, password2)
        validate_password_strength(password)
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user
