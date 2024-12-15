from rest_framework import serializers
from users_app.models import CustomUser
from .models import Game



class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]

class GameSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Game
        fields = ["id", "name", "price", "author"]
