# Generated by Django 3.2.11 on 2022-04-02 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0041_alter_orderlist_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='order_note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
