from rest_framework import viewsets
from helpers import SerializerFactory
from .serializers import *
from .models import *
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = SerializerFactory(
        default=UserSerializer,
        create=UserRegisterSerializer
    )
    lookup_field = "username"
   

    def get_permissions(self):
        if self.action == 'destroy' or 'update':
            return [CanDeleteOnlySelf()]
        return super().get_permissions()



