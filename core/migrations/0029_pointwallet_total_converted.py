# Generated by Django 3.2.11 on 2022-06-13 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_winningchance_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointwallet',
            name='total_converted',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]