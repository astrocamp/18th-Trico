from django.db import models
from django.contrib.auth.models import User
from services.models import Service
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django_fsm import FSMField, transition


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("credit_card", "Credit Card"),
        ("atm", "ATM"),
        ("linepay", "Line Pay"),
        ("googlepay", "Google Pay"),
        ("barcode", "Barcode"),
    ]

    PLAN_CHOICES = [
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]

    # 用戶和服務關聯
    client_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders_as_client",
        verbose_name="客戶",
        null=True,
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        related_name="orders",
        verbose_name="服務",
        null=True,
        blank=True,
    )

    # 訂單相關
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="訂單日期")
    total_price = models.PositiveIntegerField(
        verbose_name="總金額",
        validators=[MinValueValidator(1), MaxValueValidator(9999999999)],
    )
    
    # 有限狀態機
    status = FSMField(
        default="pending", 
        choices=STATUS_CHOICES, 
        verbose_name="訂單狀態"
    )

    # 支付相關
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name="付款方式"
    )
    merchant_trade_no = models.CharField(
        max_length=30, unique=True, null=True, blank=True, verbose_name="商店訂單編號"
    )

    selected_plan = models.CharField(
        max_length=20, 
        choices=PLAN_CHOICES, 
        null=True, 
        blank=True,
        verbose_name="選擇方案")

    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = "訂單"

    def save(self, *args, **kwargs):
        if not self.merchant_trade_no:
            self.merchant_trade_no = f"ORDER{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.merchant_trade_no} - {self.client_user.username}"

    # 狀態機轉換定義
    @transition(field=status, source="pending", target="paid")
    def mark_as_paid(self):
        #將狀態從 pending 切換為 paid
        print(f"Order {self.merchant_trade_no} marked as Paid.")

    @transition(field=status, source="paid", target="completed")
    def mark_as_completed(self):
        #將狀態從 paid 切換為 completed
        print(f"Order {self.merchant_trade_no} marked as Completed.")

    @transition(field=status, source=["pending", "paid"], target="cancelled")
    def cancel_order(self):
        #將狀態從 pending 或 paid 切換為 cancelled
        print(f"Order {self.merchant_trade_no} marked as Cancelled.")
        service_title = (
            self.service.title if self.service else "N/A"
        )  # 如果沒有服務，顯示 N/A
        return f"Order {self.merchant_trade_no} - {self.client_user.username} - {service_title}"
