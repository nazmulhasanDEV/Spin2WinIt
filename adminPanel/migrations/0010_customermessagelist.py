# Generated by Django 3.2.11 on 2022-04-24 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0009_freedelivery_helpcenter_safepayment_shopwithconfidence'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerMessageList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('subj', models.CharField(max_length=255)),
                ('msg', models.CharField(max_length=255)),
            ],
        ),
    ]