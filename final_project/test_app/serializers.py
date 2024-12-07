from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]


class BookSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
