from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    author_details = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["id", "name", "price", "author", "author_details"]

    def get_author_details(self, obj):
        return {"id": obj.author.id, "name": obj.author.username}
