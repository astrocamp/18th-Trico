from django.db import models
from django.contrib.auth.models import User
import shortuuid


class ChatGroup(models.Model):
    group_name = models.CharField(
        max_length=128, unique=True, default=shortuuid.uuid
    )  # 默認使用 UUID
    users_online = models.ManyToManyField(
        User, related_name="online_in_groups", blank=True
    )
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)
    is_private = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # 確保 group_name 是唯一的 UUID
        if not self.group_name:
            self.group_name = shortuuid.uuid()
        super().save(*args, **kwargs)

    @staticmethod
    def get_or_create_group_for_users(users):
        """
        確保用戶之間的唯一聊天群組，並保持 UUID 作為 group_name
        """
        # 查找是否已有群組
        existing_groups = ChatGroup.objects.filter(is_private=True)
        for group in existing_groups:
            if set(group.members.all()) == set(users):
                return group  # 如果找到匹配的群組，直接返回

        # 創建新群組，默認使用 UUID
        new_group = ChatGroup.objects.create()
        new_group.members.set(users)
        new_group.save()
        return new_group

    def user_can_access(self, user):
        """檢查用戶是否有權限訪問此聊天組"""
        return self.members.filter(id=user.id).exists()

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(
        ChatGroup, related_name="chat_messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    is_unread = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.author.username}: {self.body}"
