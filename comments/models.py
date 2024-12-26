from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title}: {self.content[:20]}"
