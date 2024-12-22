from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r"wallet", WalletViewSet, basename="wallet")


urlpatterns = [
    path("", include(router.urls)),
]
