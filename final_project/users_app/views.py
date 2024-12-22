from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from helpers import (
    SerializerFactory,
    CanDeleteOnlySelf,
)
from .serializers import *
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.get_user_with_all_details()
    serializer_class = SerializerFactory(
        default=UserSerializer,
        create=UserRegisterSerializer,
    )
    lookup_field = "username"
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        if self.action in ["destroy", "update", "partial_update"]:
            return [CanDeleteOnlySelf()]
        return super().get_permissions()
