# Generated by Django 3.2.11 on 2022-04-16 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0067_delete_woocommerceprodctimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannerlist',
            name='offer_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]