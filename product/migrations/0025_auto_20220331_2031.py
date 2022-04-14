# Generated by Django 3.2.11 on 2022-03-31 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0024_auto_20220329_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_list',
            name='about_store',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='new_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='old_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='product_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='product_thumbnail_img'),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='short_des',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
