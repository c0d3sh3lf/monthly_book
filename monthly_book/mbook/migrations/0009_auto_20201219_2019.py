# Generated by Django 3.1.3 on 2020-12-19 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mbook', '0008_auto_20201218_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_code',
            field=models.CharField(default='0', max_length=191, null=True),
        ),
    ]