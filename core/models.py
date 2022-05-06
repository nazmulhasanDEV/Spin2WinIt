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


# user credit wallet
class CreditWallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True)
    available = models.CharField(max_length=255, default='0')
    purchased = models.CharField(max_length=255, default='0')#unnecessary
    spent = models.CharField(max_length=255, default='0')
    spent_amount = models.CharField(max_length=255, blank=True, null=True, default='0') # unnecessary

    def __str__(self):
        return self.user.email + " || " + self.available

# user credit purchasing history
class CreditPurchasingHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    purchased_credit_amnt = models.CharField(max_length=255, blank=True, null=True)
    paid_amount = models.CharField(max_length=255, blank=True, null=True) # in usd

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
        return self.user.email + '||' + self.purchased_credit_amnt + "||" + self.paid_amount


# number of chance to play/spin the game
class WinningChance(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    remaining_chances = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email

# Winning chance purchasing history
class WinningChancePurchasingHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    point_charged = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.CharField(max_length=255, blank=True, null=True)
    chance_purchased = models.CharField(max_length=255, blank=True, null=True)

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
        return self.user.email


# user won prizes
class PrizeList(models.Model):
    user = models.ForeignKey(Account,  on_delete=models.CASCADE)
    pirze = models.CharField(max_length=255, default='')
    product_as_prize = models.ForeignKey(ProductList, on_delete=models.PROTECT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.email


