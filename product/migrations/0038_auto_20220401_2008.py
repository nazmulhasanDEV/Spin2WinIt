# Generated by Django 3.2.11 on 2022-04-01 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_alter_cart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
