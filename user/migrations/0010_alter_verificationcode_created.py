# Generated by Django 3.2.11 on 2022-02-26 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_verificationcode_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
