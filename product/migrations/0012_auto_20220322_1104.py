# Generated by Django 3.2.11 on 2022-03-22 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_woocommerceprodctimages_woocommerceproductlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='woocommerceproductlist',
            name='avrg_rating',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='woocommerceproductlist',
            name='rating_count',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]