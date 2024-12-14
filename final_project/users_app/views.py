from rest_framework import viewsets
from helpers import SerializerFactory
from rest_framework.views import APIView
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
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
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerFactory(
        default=WalletSerializer,
    )
    queryset = Wallet.objects.all()

    @action(detail=True, methods=['post'], url_path='add_money')
    def add_money(self, request, pk=None):
        user = request.user
        amount = Decimal(request.data.get("money", 0))
        if amount <= 0:
            return Response({"error": "Amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wallet = Wallet.objects.add_money_to_wallet(user, amount)
            return Response(
                {"message": f"{amount} added to your wallet.", "current_balance": wallet.money},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=True, methods=['post'], url_path='pay_money')
    def pay_money(self,request,pk=None):
        user=request.user
        amount = Decimal(request.data.get("money", 0))
        current_money=Wallet.objects.get_current_money_by_user(user=user)
        if current_money < amount:
            return Response({"error": "you dont have enough money"}, status=status.HTTP_400_BAD_REQUEST)
        if amount <= 0:
            return Response({"error": "Amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wallet = Wallet.objects.pay_money_from_wallet(user, amount)
            return Response(
                {"message": f"{amount} added to your wallet.", "current_balance": wallet.money},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

   
