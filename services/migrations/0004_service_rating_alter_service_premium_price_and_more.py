# Generated by Django 5.1.4 on 2024-12-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0003_service_premium_delivery_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="rating",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                default=None,
                help_text="Client rating for the service (e.g., 4.5 stars)",
                max_digits=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="premium_price",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="service",
            name="standard_price",
            field=models.PositiveIntegerField(),
        ),
    ]