# Generated by Django 3.2.11 on 2022-05-11 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_prizelist_prize_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prizelist',
            options={'ordering': ['-pk']},
        ),
    ]