# Generated by Django 5.1.4 on 2025-01-13 10:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("comments", "0001_initial"),
        ("services", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="service",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="services.service",
            ),
        ),
        migrations.AddConstraint(
            model_name="comment",
            constraint=models.UniqueConstraint(
                fields=("user", "service"), name="unique_comment"
            ),
        ),
    ]