from rest_framework import viewsets
from helpers import SerializerFactory
from rest_framework.views import APIView
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
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


class WalletViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):

    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.get_wallet_by_user(request.user)
            return Response(
                {"current_balance": wallet.money}, status=status.HTTP_200_OK
            )
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        user = request.user
        print(user)
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
