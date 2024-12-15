from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from .serializers import *
from .models import *



class GameViewSet(viewsets.ModelViewSet):
    serializer_class=GameSerializer
    queryset= Game.objects.all()
    lookup_field='name'