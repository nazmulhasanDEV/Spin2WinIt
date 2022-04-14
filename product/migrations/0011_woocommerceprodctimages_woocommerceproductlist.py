# Generated by Django 3.2.11 on 2022-03-21 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_product_list_policy_followed'),
    ]

    operations = [
        migrations.CreateModel(
            name='WoocommerceProdctImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=255)),
                ('img1', models.ImageField(blank=True, null=True, upload_to='woocommerce_pridct_imgs')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='woocommerce_pridct_imgs')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='woocommerce_pridct_imgs')),
                ('img4', models.ImageField(blank=True, null=True, upload_to='woocommerce_pridct_imgs')),
                ('img5', models.ImageField(blank=True, null=True, upload_to='woocommerce_pridct_imgs')),
            ],
        ),
        migrations.CreateModel(
            name='WoocommerceProductList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(default='', max_length=255)),
                ('name', models.TextField()),
                ('slug', models.TextField()),
                ('description', models.TextField()),
                ('price', models.CharField(default='', max_length=255)),
                ('regular_price', models.CharField(blank=True, max_length=255, null=True)),
                ('total_sales', models.CharField(blank=True, max_length=255, null=True)),
                ('cat_id', models.CharField(max_length=255)),
                ('cat_name', models.CharField(max_length=255)),
                ('subcat_id', models.CharField(blank=True, max_length=255, null=True)),
                ('subcat_name', models.CharField(blank=True, max_length=255, null=True)),
                ('stock_status', models.CharField(max_length=255)),
            ],
        ),
    ]
