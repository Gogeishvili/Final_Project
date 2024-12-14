from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")
router.register(r"bookModels", views.BookModelViewSet, basename="bookModels")


urlpatterns = [
    path("", include(router.urls)),
    path("books/", views.BookViewSet.as_view()),
]
