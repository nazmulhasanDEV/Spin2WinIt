# Generated by Django 3.2.11 on 2022-03-31 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_auto_20220331_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_list',
            name='title',
            field=models.TextField(blank=True, default='title', null=True),
        ),
    ]