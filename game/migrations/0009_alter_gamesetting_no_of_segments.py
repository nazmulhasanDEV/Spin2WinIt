# Generated by Django 3.2.11 on 2022-03-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_alter_segmentlist_segment_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesetting',
            name='no_of_segments',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]