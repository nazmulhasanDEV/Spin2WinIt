# Generated by Django 3.2.11 on 2022-05-14 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0007_userprofileads_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileads',
            name='banner_img',
            field=models.ImageField(blank=True, null=True, upload_to='user_profile_ads_bnnr'),
        ),
    ]