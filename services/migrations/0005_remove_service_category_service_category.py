# Generated by Django 5.1.4 on 2024-12-31 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_rename_updated_at_category_created_at"),
        ("services", "0004_service_rating_alter_service_premium_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="service",
            name="category",
        ),
        migrations.AddField(
            model_name="service",
            name="category",
            field=models.ManyToManyField(
                related_name="services", to="categories.category"
            ),
        ),
    ]