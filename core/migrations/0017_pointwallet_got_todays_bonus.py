# Generated by Django 3.2.11 on 2022-05-25 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_prizelist_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointwallet',
            name='got_todays_bonus',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]