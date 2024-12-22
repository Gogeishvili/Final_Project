from rest_framework import serializers
from .models import *


class CartSerilizer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    games = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "games"]

    def get_games(self, obj):
        return [
            {"id": game.id, "name": game.name, "price": game.price}
            for game in obj.games.all()
        ]


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    game = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ["id", "user", "game"]

    def get_game(self, obj):

        return {
            "id": obj.game.id,
            "name": obj.game.name,
            "price": obj.game.price,
        }


class MostSoldGameSerializer(serializers.Serializer):
    game_name = serializers.CharField(source="game__name")
    sold_count = serializers.IntegerField()
