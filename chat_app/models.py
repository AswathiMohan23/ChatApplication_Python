from django.db import models

from user.models import UserModel


class UserChat(models.Model):
    group_name = models.CharField(max_length=40)
    message = models.TextField(blank=True, default="")
    user = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_chat'
