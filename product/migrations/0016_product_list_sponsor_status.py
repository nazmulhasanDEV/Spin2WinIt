# Generated by Django 3.2.11 on 2022-03-23 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20220323_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_list',
            name='sponsor_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
