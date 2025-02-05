from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Chat(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="chats")


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
