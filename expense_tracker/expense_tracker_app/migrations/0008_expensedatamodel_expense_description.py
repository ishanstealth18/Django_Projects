# Generated by Django 4.2.6 on 2024-09-20 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker_app', '0007_alter_expensedatamodel_expense_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensedatamodel',
            name='expense_description',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
