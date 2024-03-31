# Generated by Django 4.2.6 on 2024-03-07 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop', '0004_rename_customer_id_orders_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Eshop.customers'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Eshop.product'),
        ),
    ]
