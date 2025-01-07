from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="姓名")
    email = models.EmailField(verbose_name="電子郵件")
    message = models.TextField(verbose_name="訊息內容")
    reply = models.TextField(
        blank=True, null=True, verbose_name="回覆內容"
    )  # 管理員回覆
    is_replied = models.BooleanField(
        default=False, verbose_name="是否已回覆"
    )  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="訊息時間")

    def __str__(self):
        return (
            f"{self.name} ({self.email}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
