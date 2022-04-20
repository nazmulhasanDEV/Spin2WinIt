from django.db import models
from user.models import Account

# banner at product details page
class BannerProdDetail(models.Model):
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    img = models.ImageField(upload_to='Product_details_pg_bnr')
    link = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.banner_id

# banner at shop page
class ShopPageBanner(models.Model):
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    img = models.ImageField(upload_to='shopPageBanner')
    link = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.banner_id

