# Generated by Django 3.1.3 on 2020-12-17 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mbook', '0005_auto_20201217_1115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='prodcut_desc',
            new_name='product_desc',
        ),
    ]
