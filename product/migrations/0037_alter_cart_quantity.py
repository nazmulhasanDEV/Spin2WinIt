# Generated by Django 3.2.11 on 2022-04-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_alter_wishlist_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, max_length=255, null=True),
        ),
    ]
