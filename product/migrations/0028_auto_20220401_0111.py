# Generated by Django 3.2.11 on 2022-03-31 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_auto_20220401_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_list',
            name='cat_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product_list',
            name='cat_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product_list',
            name='subcat_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product_list',
            name='subcat_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]