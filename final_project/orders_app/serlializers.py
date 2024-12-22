from rest_framework import serializers
from users_app.models import CustomUser
from games_app.models import Game
from .models import *


class UserNestedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username"]


class GameNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["name", "price"]


class CartSerilizer(serializers.ModelSerializer):
    user = UserNestedeSerializer()
    games = GameNestedSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "games"]


class GameNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "name", "price"]


class PurchaseSerializer(serializers.ModelSerializer):
    user = UserNestedeSerializer()
    game = GameNestedSerializer()

    class Meta:
        model = Purchase
        fields = ["id", "user", "game"]


class MostSoldGameSerializer(serializers.Serializer):
    game_name = serializers.CharField(source="game__name")
    sold_count = serializers.IntegerField()
