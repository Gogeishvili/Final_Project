from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]


class BookSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()


class BookModelSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BookModel
        fields = "__all__"

    def get_total_price(self, obj):
        return BookModel.objects.get_total_price(obj.id)
    
    


