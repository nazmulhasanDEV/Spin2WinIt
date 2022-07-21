# Generated by Django 3.2.11 on 2022-03-28 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_allproductlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_list',
            name='product_type',
            field=models.CharField(blank=True, choices=[('wsp', 'Woocommerce store product'), ('mcp', 'Custom Product')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product_list',
            name='woocmrce_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.woocommerceproductlist'),
        ),
    ]