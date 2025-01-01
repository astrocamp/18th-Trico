# Generated by Django 5.1.4 on 2025-01-01 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_alter_order_payment_method_alter_order_total_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="selected_plan",
            field=models.CharField(
                blank=True,
                choices=[("standard", "Standard"), ("premium", "Premium")],
                max_length=20,
                null=True,
                verbose_name="選擇方案",
            ),
        ),
    ]
