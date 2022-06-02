from django.db import models
from user.models import Account
from product.models import *
from core.models import *

# seller collections/collected product list
class SellerCollections(models.Model):
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.seller.email + '||' + self.product.title

# seller bought packages
class SellerPurchasedPackages(models.Model):
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    package = models.ForeignKey(PackageList, on_delete=models.CASCADE)
    paid_amount = models.CharField(max_length=20, blank=True, null=True)

    # payment details

    # payee infomations
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payee_email = models.CharField(max_length=255, blank=True, null=True)
    payee_marchnt_id = models.CharField(max_length=255, blank=True, null=True)
    payee_address = models.CharField(max_length=255, blank=True, null=True)

    # payeer infor
    payer_name = models.CharField(max_length=255, blank=True, null=True)
    payer_email = models.CharField(max_length=255, blank=True, null=True)
    payer_id = models.CharField(max_length=255, blank=True, null=True)
    payer_post_code = models.CharField(max_length=255, blank=True, null=True)
    payer_country_code = models.CharField(max_length=255, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.seller.email + ' || ' + self.package.name.name
