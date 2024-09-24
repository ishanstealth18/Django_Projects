# Generated by Django 4.2.6 on 2024-09-23 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker_app', '0008_expensedatamodel_expense_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensedatamodel',
            name='expense_amount',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='expensedatamodel',
            name='expense_date',
            field=models.DateField(max_length=10),
        ),
    ]