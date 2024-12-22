from rest_framework import serializers
from users_app.models import CustomUser
from .models import Game


class AuthorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]


class GameViewSerializer(serializers.ModelSerializer):
    author = AuthorNestedSerializer()

    class Meta:
        model = Game
        fields = ["id", "name", "price", "author"]


class GameCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ["name", "price", "author"]


class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["price"]
