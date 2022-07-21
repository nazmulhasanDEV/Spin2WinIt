# Generated by Django 3.2.11 on 2022-04-02 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0039_cart_total_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('shipping_date', models.DateTimeField(blank=True, null=True)),
                ('order_status', models.CharField(blank=True, choices=[('a', 'Approved'), ('p', 'Pending')], max_length=255, null=True)),
                ('delivery_status', models.BooleanField(blank=True, default=False, null=True)),
                ('items', models.ManyToManyField(blank=True, null=True, to='product.Cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]