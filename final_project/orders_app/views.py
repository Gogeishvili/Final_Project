from django.db.models import Count
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from helpers.validators import *
from wallet_app.models import Wallet
from .serlializers import *
from .models import Cart


class CartViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = CartSerilizer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"], url_path="purchase")
    def purchase(self, request, pk=None):
        user = request.user

        try:
            cart = Cart.objects.get(id=pk)
            if cart.user != user:
                return Response(
                    {"error": "You are not authorized to purchase this cart."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if not cart.games.exists():
                return Response(
                    {"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST
                )

            total_cost = sum(game.price for game in cart.games.all())

            current_money = Wallet.objects.get_current_money_by_user(user=user)
            validate_enogh_amount(current_money, total_cost)
            Wallet.objects.pay_money_from_wallet_by_user(user, total_cost)

            purchases = [Purchase(user=user, game=game) for game in cart.games.all()]
            Purchase.objects.bulk_create(purchases)

            cart.games.clear()

            return Response(
                {"message": "Purchase completed successfully."},
                status=status.HTTP_200_OK,
            )

        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="most_sold_games")
    def most_sold_games(self, request):
        most_sold_games = (
            Purchase.objects.values("game__name")
            .annotate(sold_count=Count("game"))
            .order_by("-sold_count")
        )

        serializer = MostSoldGameSerializer(most_sold_games, many=True)
        return Response(serializer.data)
