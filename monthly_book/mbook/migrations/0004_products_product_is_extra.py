# Generated by Django 3.1.3 on 2020-11-28 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mbook', '0003_auto_20201125_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_is_extra',
            field=models.BooleanField(default=False),
        ),
    ]
