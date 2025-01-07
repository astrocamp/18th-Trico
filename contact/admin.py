from django.contrib import admin
from django.core.mail import send_mail
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_replied")
    search_fields = ("name", "email", "message")
    list_filter = ("is_replied", "created_at")
    ordering = ("-created_at",)
    actions = ["send_reply"]

    def send_reply(self, request, queryset):
        for message in queryset:
            if message.reply and not message.is_replied:
                send_mail(
                    subject=f"回覆您的聯繫訊息",
                    message=f"您好 {message.name}，\n\n這是我們的回覆：\n\n{message.reply}",
                    from_email=None,  # 使用 DEFAULT_FROM_EMAIL
                    recipient_list=[message.email],
                )
                message.is_replied = True  
                message.save()
        self.message_user(request, "回覆已成功發送！")

    send_reply.short_description = "發送回覆到用戶電子郵件"
