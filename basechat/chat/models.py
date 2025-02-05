from asgiref.sync import sync_to_async
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

    async def websocket_receive(self, event):
        user = self.scope["user"]

        if user.is_authenticated:
            try:
                print(f"User from scope: {user} (type: {type(user)})")
                user_instance = await sync_to_async(User.objects.get)(pk=user.pk)  # Асинхронный запрос к БД
            except User.DoesNotExist:
                await self.send({"type": "websocket.close"})
                return

            message = await sync_to_async(Message.objects.create)(
                sender=user_instance,
                chat=self.chat,
                content=event["text"]
            )

            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    "type": "chat.message",
                    "message": event["text"],
                    "sender": user_instance.username
                }
            )
        else:
            await self.send({"type": "websocket.close"})
