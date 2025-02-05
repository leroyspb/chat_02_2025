from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import ChatViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"chats", ChatViewSet)
router.register(r"messages", MessageViewSet)

urlpatterns = [
    path('', views.index, name="chat"),
    path("", include(router.urls)),
]
