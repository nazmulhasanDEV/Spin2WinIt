from django.db import models
from user.models import Account
from product.models import ProductList

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

# banner at shop page by category
class ShopPageBanner(models.Model):
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    img = models.ImageField(upload_to='shopPageBanner')
    link = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.banner_id

# banner/product advertisement on user profile page
class UserProfileAds(models.Model):

    ADS_TYPE = (
        ('banner', 'Banner'),
        ('product', 'Product'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    ads_type = models.CharField(choices=ADS_TYPE, max_length=25)
    banner_img = models.ImageField(blank=True, null=True, upload_to='user_profile_ads_bnnr')
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.ads_type


