from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="custom_users_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_users_permissions", blank=True)
