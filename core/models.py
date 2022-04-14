from django.db import models
from user.models import Account
from product.models import *


# user wallet
class PointWallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    available = models.CharField(max_length=255, default='0')
    purchased = models.CharField(max_length=255, default='0')
    spent     = models.CharField(max_length=255, default='0')
    spent_amount = models.CharField(max_length=255, blank=True, null=True, default='0')

    def __str__(self):
        return self.user.email

# number of chance to play/spin the game
class WinningChance(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    remaining_chances = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email

# user won prizes
class PrizeList(models.Model):
    user = models.ForeignKey(Account,  on_delete=models.CASCADE)
    pirze = models.CharField(max_length=255, default='')
    product_as_prize = models.ForeignKey(ProductList, on_delete=models.PROTECT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.email


