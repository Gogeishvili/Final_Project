from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from helpers import (
    SerializerFactory,
    CanDeleteOnlySelf,
    validate_positive_amount,
    validate_enogh_amount,
    IsAuthorOrReadOnly
)
from .serializers import *
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.get_user_with_all_details()
    serializer_class = SerializerFactory(
        default=UserSerializer,
        create=UserRegisterSerializer,
    )
    lookup_field = "username"

    def get_permissions(self):
        if self.action in ["destroy", "update",'partial_update']:
            return [CanDeleteOnlySelf()]
        return super().get_permissions()


class WalletViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerFactory(
        default=WalletNestedSerializer,
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
