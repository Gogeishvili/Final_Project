from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from helpers import validate_string_match, validate_password_strength
from .models import *


class CartSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"


