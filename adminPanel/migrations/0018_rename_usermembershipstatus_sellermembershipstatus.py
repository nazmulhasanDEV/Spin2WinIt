# Generated by Django 3.2.11 on 2022-05-29 14:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminPanel', '0017_usermembershipstatus'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserMembershipStatus',
            new_name='SellerMembershipStatus',
        ),
    ]