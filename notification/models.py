from django.db import models
from django.urls import reverse
from services.models import Service


class Notification(models.Model):
    recipient = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="actor_notifications"
    )
    verb = models.CharField(max_length=255)  # 動作描述，例如 "點贊"
    description = models.TextField(null=True, blank=True)  # 通知描述
    target_service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )
    unread = models.BooleanField(default=True)  # 是否為未讀通知
    timestamp = models.DateTimeField(auto_now_add=True)  # 通知的時間

    def __str__(self):
        return f"{self.actor} {self.verb} -> {self.recipient}"

    def get_target_url(self):
        """
        返回通知指向的目標服務的 URL
        """
        if self.target_service:
            return reverse(
                "services:service_detail",
                kwargs={"id": self.recipient.id, "service_id": self.target_service.id},
            )
        return "#"
