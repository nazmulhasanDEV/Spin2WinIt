# Generated by Django 3.2.11 on 2022-03-26 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0005_cookiepolicy_deliverypolicy_privacypolicy_refundpolicy_returnpolicy_securitypolicy_termsconditions'),
        ('product', '0021_bannerlist_banner_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_list',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminPanel.productcategory'),
        ),
        migrations.AlterField(
            model_name='product_list',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminPanel.productsubcategory'),
        ),
    ]