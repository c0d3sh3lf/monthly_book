# Generated by Django 3.1.3 on 2020-12-18 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mbook', '0006_auto_20201217_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_barcode',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='products',
            name='product_type',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
