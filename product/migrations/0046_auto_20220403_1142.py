# Generated by Django 3.2.11 on 2022-04-03 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20220403_1142'),
        ('product', '0045_ordereditem_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='billing_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.billinginfo'),
        ),
        migrations.AddField(
            model_name='orderlist',
            name='shipping_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.shippinginfo'),
        ),
    ]