# Generated by Django 3.2.11 on 2022-04-08 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0058_alter_product_list_productimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='woocommerceproductlist',
            name='product_img',
            field=models.ManyToManyField(blank=True, null=True, to='product.ProductImg'),
        ),
    ]