# Generated by Django 3.2.11 on 2022-05-22 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_auto_20220522_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprizedeliverorder',
            name='items',
            field=models.ManyToManyField(blank=True, to='game.CurrentDelivryRequestPrizeProduct'),
        ),
    ]
