# Generated by Django 4.2.6 on 2024-05-27 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_library_app', '0006_addbookmodel_contributed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addbookmodel',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
