from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.contrib.auth.password_validation import validate_password
from helpers import validate_string_match,validate_password_strength
from .models import *

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["money"]


class UserSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email","wallet"]


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True, required=True, label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        validate_string_match(password, password2)
        validate_password_strength(password)
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user




