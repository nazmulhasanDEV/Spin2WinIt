# Generated by Django 3.2.11 on 2022-04-02 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_ordereditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='items',
            field=models.ManyToManyField(blank=True, to='product.OrderedItem'),
        ),
    ]
