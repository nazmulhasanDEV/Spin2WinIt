# Generated by Django 3.2.11 on 2022-03-31 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20220401_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_list',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product_list',
            name='regular_price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
