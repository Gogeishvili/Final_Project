from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import *
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"


class BookViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        books = [Book(name="Book 1", price=29), Book(name="Book 2", price=19)]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            data = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
