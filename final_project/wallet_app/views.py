from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from decimal import Decimal
from helpers import (
    SerializerFactory,
    validate_positive_amount,
    validate_enogh_amount,
)
from .serializers import *
from .models import *


class WalletViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerFactory(
        default=WalletSerializer,
    )
    queryset = Wallet.objects.all()

    @action(detail=False, methods=["post"], url_path="add_money")
    def add_money(self, request):
        user = request.user
        amount = Decimal(request.data.get("money", 0))

        try:
            validate_positive_amount(amount)

            wallet = Wallet.objects.add_money_to_wallet_by_user(user, amount)
            return Response(
                {
                    "message": f"{amount} added to your wallet.",
                    "current_balance": wallet.money,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="pay_money")
    def pay_money(self, request):
        user = request.user
        amount = Decimal(request.data.get("money", 0))
        current_money = Wallet.objects.get_current_money_by_user(user=user)
        try:
            validate_positive_amount(amount)
            validate_enogh_amount(current_money, amount)

            wallet = Wallet.objects.pay_money_from_wallet_by_user(user, amount)

            return Response(
                {
                    "message": f"{amount} deducted from your wallet.",
                    "current_balance": wallet.money,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
