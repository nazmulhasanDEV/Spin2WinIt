# Generated by Django 3.2.11 on 2022-04-10 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0061_auto_20220410_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]