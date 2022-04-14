# Generated by Django 3.2.11 on 2022-03-25 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_gamesetting_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='segmentlist',
            name='point_as_prize',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.pointas_prize'),
        ),
        migrations.AddField(
            model_name='segmentlist',
            name='product_as_prize',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.sponsoredproductforprize'),
        ),
    ]
