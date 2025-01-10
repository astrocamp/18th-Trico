from django.db import models
from django.contrib.auth.models import User
from services.models import Service
from django.core.validators import MaxValueValidator, MinValueValidator

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="comments"
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    content = models.TextField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "service"], name="unique_comment"
            )
        ]  

    def __str__(self):
        return self.content[:20]
