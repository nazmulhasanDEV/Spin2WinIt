from django.db import models
from user.models import Account
from product.models import *
from adminPanel.models import *


# user wallet
class PointWallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    available = models.IntegerField(default=0, blank=True, null=True)
    purchased = models.IntegerField(default=0, blank=True, null=True)
    spent     = models.CharField(max_length=255, default='0') # unnecessary
    spent_amount = models.CharField(max_length=255, blank=True, null=True, default='0') # unnecessay
    total_converted = models.IntegerField(default=0, blank=True, null=True)
    got_todays_bonus = models.BooleanField(default=False, blank=True, null=True)

    total_pointsOf_crnt_user = models.IntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_pointsOf_crnt_user = self.available + self.total_converted
        super(PointWallet, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email

class PointToCreditConversionHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    converted_point_amount = models.IntegerField(default=0)
    got_credit_amount = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + "||" + str(self.converted_point_amount) + "||" + str(self.got_credit_amount)

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
    available = models.IntegerField(default=0, blank=True, null=True)
    purchased = models.IntegerField(default=0, blank=True, null=True)#unnecessary
    spent = models.IntegerField(default=0, blank=True, null=True)
    total_credts_ofCurrentUser = models.IntegerField(default=0, blank=True, null=True)


    def save(self, *args, **kwargs):
        self.total_credts_ofCurrentUser = self.available + self.spent
        super(CreditWallet, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email + " || " + str(self.available)

# user credit purchasing history
class CreditPurchasingHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    purchased_credit_amnt = models.CharField(max_length=255, blank=True, null=True)
    paid_amount = models.FloatField(default=0, blank=True, null=True) # in usd

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
        return self.user.email + '||' + str(self.purchased_credit_amnt) + "||" + str(self.paid_amount)


# number of chance/spin tokens to play/spin the game
class WinningChance(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    remaining_chances = models.IntegerField(default=0, blank=True, null=True)
    purchased = models.IntegerField(default=0, blank=True, null=True)
    spent = models.IntegerField(default=0, blank=True, null=True)
    total_spin_tokens_of_crnt_usr = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_spin_tokens_of_crnt_usr = self.remaining_chances + self.spent
        super(WinningChance, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email

# Winning chance/spin token purchasing history
class WinningChancePurchasingHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    point_charged = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.FloatField(default=0, blank=True, null=True)
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
    isAddedToCartOption=(
        ('yes', "Yes"),
        ('no', "No")
    )
    user = models.ForeignKey(Account,  on_delete=models.CASCADE)
    prize_type = models.CharField(max_length=10, default='', choices=option)
    pirze = models.CharField(max_length=255, default='') # prize as ponts
    product_as_prize = models.ForeignKey(ProductList, on_delete=models.PROTECT, blank=True, null=True)
    delivery_status = models.BooleanField(default=False, blank=True, null=True)# not necessary
    status = models.BooleanField(default=False, blank=True, null=True) # this is used for delivery status
    isSentToCart = models.BooleanField(blank=True, null=True)# not necessary
    isAddedToCart = models.CharField(max_length=232, choices=isAddedToCartOption, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        if self.prize_type  == 'point':
            self.delivery_status = True
            self.status = True
            super(PrizeList, self).save(*args, **kwargs)
        else:
            self.delivery_status = False
            self.status = False
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
