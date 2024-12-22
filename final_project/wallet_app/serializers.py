from rest_framework import serializers
from .models import *


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username"]


class WalletSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "money", "user"]
