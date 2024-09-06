# Generated by Django 4.2.6 on 2024-08-30 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_category', models.CharField(max_length=100)),
                ('expense_amount', models.IntegerField()),
                ('expense_date', models.DateTimeField()),
            ],
        ),
    ]