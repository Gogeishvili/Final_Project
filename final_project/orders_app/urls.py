from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r"carts", CartViewSet, basename="carts")
router.register(r"purchase", PurchaseViewSet, basename="purchase")



urlpatterns = [
    path("", include(router.urls)),
]