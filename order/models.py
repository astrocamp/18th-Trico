# orders/models.py
from django.db import models
import uuid


class Order(models.Model):
    client_user_id = models.IntegerField()  # 客戶 ID
    service_id = models.IntegerField()  # 服務 ID
    order_date = models.DateTimeField(auto_now_add=True)  # 訂單建立時間
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 訂單金額
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Paid", "Paid"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending",
    )  # 訂單狀態
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("CreditCard", "Credit Card"),
            ("ATM", "ATM"),
            ("Other", "Other"),
        ],
        default="CreditCard",
    )  # 付款方式
    merchant_trade_no = models.CharField(
        max_length=30, unique=True, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.merchant_trade_no:
            # 自動生成 MerchantTradeNo
            self.merchant_trade_no = f"ORDER{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.merchant_trade_no}"
