# Generated by Django 3.2.11 on 2022-05-14 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0005_userprofileads'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileads',
            name='added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]