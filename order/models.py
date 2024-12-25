# orders/models.py
from django.db import models


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

    def __str__(self):
        return f"Order {self.id}"
