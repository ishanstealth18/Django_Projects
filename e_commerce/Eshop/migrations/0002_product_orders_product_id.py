# Generated by Django 4.2.6 on 2024-01-25 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=155)),
                ('description', models.TextField()),
                ('images', models.ImageField(upload_to='images/')),
                ('price', models.IntegerField()),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eshop.category')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='product_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Eshop.product'),
            preserve_default=False,
        ),
    ]
