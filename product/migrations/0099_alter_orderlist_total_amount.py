# Generated by Django 3.2.11 on 2022-06-12 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0098_alter_orderlist_total_shipping_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='total_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]