from django.db import models
from user.models import Account
from product.models import *
from adminPanel.models import *


# user wallet
class PointWallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    available = models.CharField(max_length=255, default='0')
    purchased = models.CharField(max_length=255, default='0')
    spent     = models.CharField(max_length=255, default='0')
    spent_amount = models.CharField(max_length=255, blank=True, null=True, default='0')
    got_todays_bonus = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.user.email

# bonus for sending referal link
class ReferalBonusList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    point_amnt = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + '||' + self.point_amnt

# dailly sign in bonus model # daily sign in bonus is fifty(50)
class GivenDailySignInBonusUsrList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + "||" + str(50) + " || " + str(self.created)

# 1000 bonus point for registering on platform
class BonusPoinForRegistration(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    point_amnt = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + '||' + str(self.point_amnt)

# bonus point model for daily email invitation
class EmailInvitationBonusUserList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.CharField(default='', max_length=255, blank=True)
    mail_to = models.CharField(default='', max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + "||" + self.amount


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


# number of chance/spin tokens to play/spin the game
class WinningChance(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    remaining_chances = models.CharField(max_length=255)
    purchased = models.CharField(default='', blank=True, null=True, max_length=255)
    spent = models.CharField(default='', blank=True, null=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.email

# Winning chance/spin token purchasing history
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
    option = (
        ('point', 'Point'),
        ('product', 'Product'),
    )
    user = models.ForeignKey(Account,  on_delete=models.CASCADE)
    prize_type = models.CharField(max_length=10, default='', choices=option)
    pirze = models.CharField(max_length=255, default='') # prize as ponts
    product_as_prize = models.ForeignKey(ProductList, on_delete=models.PROTECT, blank=True, null=True)
    delivery_status = models.BooleanField(default=False, blank=True, null=True)# not necessary
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        if self.prize_type  == 'point':
            self.delivery_status = True
            super(PrizeList, self).save(*args, **kwargs)
        else:
            self.delivery_status = False
            super(PrizeList, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email


# package list
class PackageList(models.Model):
    package_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.ForeignKey(PackageNameList, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    old_price = models.FloatField(default=0.0)
    options = models.ManyToManyField(PackageOptions)
    products = models.ManyToManyField(ProductList)

    status = models.BooleanField(default=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.package_id = self.package_id + str(self.pk)
        super(PackageList, self).save(*args, **kwargs)

    def __str__(self):
        return self.name.name + "||" + str(self.price)

# user email invitation history
