from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from users_app.models import Wallet
from helpers.validators import *
from .serlializers import *
from .models import Cart

class CartViewSet(mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class=CartSerilizer
    queryset=Cart.objects.all()

    @action(detail=True, methods=["get"], url_path="purchase")
    def purchase(self, request,pk=None):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
            if not cart.games.exists():
                return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
            
            total_cost = sum(game.price for game in cart.games.all())
           
           
            current_money = Wallet.objects.get_current_money_by_user(user=user)
            validate_enogh_amount(current_money, total_cost)
            Wallet.objects.pay_money_from_wallet_by_user(user, total_cost)

           
            purchases = []
            for game in cart.games.all():
                purchases.append(Purchase(user=user, game=game))
            Purchase.objects.bulk_create(purchases)

            cart.games.clear()

            return Response(
                {"message": "Purchase completed successfully."},
                status=status.HTTP_200_OK,
            )

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)