from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from helpers import SerializerFactory,IsAuthorOrReadOnly
from .serializers import *
from .models import *


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = SerializerFactory(
        default=GameViewSerializer,
        create=GameCreateSerializer,
        update=GameUpdateSerializer,
    )
    permission_classes = [IsAuthorOrReadOnly]

    queryset = Game.objects.all()
    lookup_field = "name"

    @action(detail=True, methods=["post"], url_path="add_game_cart",permission_classes=[IsAuthenticated])
    def add_game_cart(self, request):
        user = request.user
        game_id = request.data.get("game_id")

        # ვამოწმებთ, თუ არსებობს ასეთი თამაში
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ვამოწმებთ, რომ თამაში მომხმარებლის მიერ არ იყოს შექმნილი
        if game.author == user:
            raise PermissionDenied("You cannot add your own game to the cart.")

        # დაამატეთ ლოგიკა თამაშის კალათაში დამატებისთვის
        user.cart.add(game)
        # თუ ასეთი ველი არ გაქვთ, შეგიძლიათ დაამატოთ ბაზაში შესაბამისი ველი ან ცხრილი.

        return Response(
            {"message": f"Game '{game.name}' has been added to your cart."},
            status=status.HTTP_200_OK,
        )
        
