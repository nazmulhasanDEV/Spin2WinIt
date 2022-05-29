from django.db import models
from user.models import Account
from product.models import *

# seller collections/collected product list
class SellerCollections(models.Model):
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.seller.email + '||' + self.product.title