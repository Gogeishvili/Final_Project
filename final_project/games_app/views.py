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
from orders_app.models import Cart
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

    @action(detail=True, methods=["get"], url_path="add_game_cart", permission_classes=[IsAuthenticated])
    def add_game_cart(self, request, name=None):
        user = request.user
       
        try:
            game = Game.objects.get(name=name)  
        except Game.DoesNotExist:
            return Response(
                {"error": "Game not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if game.author == user:
            raise PermissionDenied("You cannot add your own game to the cart.")

       
        try:
            cart = Cart.objects.add_game_in_cart(user, game)  
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": f"Game '{game.name}' has been added to your cart."},
            status=status.HTTP_200_OK,
        )
        
