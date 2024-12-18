from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .serlializers import *
from .models import Cart

class CartViewSet(viewsets.ModelViewSet):
    serializer_class=CartSerilizer
    queryset=Cart.objects.all()

    