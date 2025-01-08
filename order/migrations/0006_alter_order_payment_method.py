# Generated by Django 5.1.4 on 2025-01-06 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_selected_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('atm', 'ATM'), ('linepay', 'Line Pay'), ('googlepay', 'Google Pay'), ('barcode', 'Barcode')], max_length=50, verbose_name='付款方式'),
        ),
    ]