# Generated by Django 3.2.11 on 2022-04-06 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_prizelist_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointwallet',
            name='spent_amount',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]