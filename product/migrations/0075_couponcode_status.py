# Generated by Django 3.2.11 on 2022-05-16 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0074_couponcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponcode',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]