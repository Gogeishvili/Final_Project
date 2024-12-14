from rest_framework import viewsets
from helpers import SerializerFactory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import *
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = SerializerFactory(
        default=UserSerializer,
        create=UserRegisterSerializer,
    )
    lookup_field = "username"

    def get_permissions(self):
        if self.action == "destroy" or "update":
            return [CanDeleteOnlySelf()]
        return super().get_permissions()


class WalletViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer

    def list(self, request):
        user = request.user
        try:
            wallet = Wallet.objects.get_wallet_by_user(user=user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found."})

        return Response({"current_balance": wallet.money})

    def create(self, request):
        user = request.user
        amount = Decimal(request.data.get("money", 0))
        if amount <= 0:
            return Response(
                {"error": "Amount must be greater than zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        wallet = Wallet.objects.add_money_to_wallet(user, amount)
        return Response(
            {
                "message": f"{amount} added to your wallet.",
                "current_balance": wallet.money,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request):
        user = request.user
        amount = Decimal(request.data.get("money", 0))

        if amount is None:
            return Response(
                {"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = Decimal(amount)
        except:
            return Response(
                {"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST
            )

        if amount <= 0:
            return Response(
                {"error": "Amount must be greater than zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            wallet = Wallet.objects.deduct_money_from_wallet(user, amount)
            return Response(
                {
                    "message": f"{amount} deducted from your wallet.",
                    "current_balance": wallet.money,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError:
            return Response(
                {"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST
            )
