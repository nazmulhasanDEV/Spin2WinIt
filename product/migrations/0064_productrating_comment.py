# Generated by Django 3.2.11 on 2022-04-10 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0063_productrating_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrating',
            name='comment',
            field=models.TextField(blank=True, default='Comment', null=True),
        ),
    ]