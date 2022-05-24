from django.db import models
from user.models import Account, UserProfilePicture
from product.models import *
from django.utils.crypto import get_random_string


# user prize list car ** *when user will move their product to cart, it will be stored here.
class PrizeCart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.PROTECT)
    confirmed_for_delivery = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.user.email

class CurrentDelivryRequestPrizeProduct(models.Model):

    option = (
        ('curnt', 'Current Order'), # curnt == current
        ('prev', 'Previous Order'), # prev == previous
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    is_current = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return "Title: " + self.product.title + " || " + str(self.user.email)


# prize deliver order
class ProductPrizeDeliverOrder(models.Model):

    option = (
        ('a', 'Approved'),
        ('p', 'Pending'),
        ('c', 'Cancel'),
    )

    payment_options = (
        ('cod', 'Cash on Delivery'),
    )

    order_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    items = models.ManyToManyField(CurrentDelivryRequestPrizeProduct, blank=True)
    sub_total_amount = models.FloatField(blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)

    start_date = models.DateTimeField(auto_now_add=True)

    order_status = models.CharField(max_length=255, choices=option, blank=True, null=True) # whether it's approved, cancelled, or Pending
    delivery_status = models.BooleanField(default=False, blank=True, null=True) # status whether customer got the product or not
    delivery_date = models.DateTimeField(blank=True, null=True)

    shipping_status = models.BooleanField(default=False, blank=True, null=True) # wheather product left from warehouse to deliver to customer
    shipping_date = models.DateTimeField(blank=True, null=True)

    order_note = models.TextField(blank=True, null=True)

    payment_status = models.BooleanField(default=False, blank=True, null=True)
    payment_options = models.CharField(max_length=35, choices=payment_options, blank=True, null=True)

    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE, blank=True, null=True)
    shipping_info = models.ForeignKey(ShippingInfo, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)



# sponsored products for game
class SponsoredProductForPrize(models.Model):
    prodct_id = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.product.title + '||' + str(self.product.product_id)


# game settings
class GameSetting(models.Model):
    no_of_segments = models.CharField(max_length=3, blank=True, null=True)
    no_of_complt_spins = models.CharField(max_length=3)
    spining_duration = models.CharField(max_length=3)
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.no_of_complt_spins +' || ' + self.no_of_segments + ' || ' + self.spining_duration

# Sponsored prize list
class PointAs_Prize(models.Model):
    point_amount = models.CharField(max_length=255)

    def __str__(self):
        return self.point_amount

# segments list
class Segment(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# segment list with prizes
class SegmentList(models.Model):
    option = (
        ('1', 'Product'),
        ('2', 'Point'),
    )
    segment_no = models.IntegerField(default=1, blank=True, null=True)

    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, blank=True, null=True)
    bg_color = models.CharField(max_length=255)
    segment_prize_type = models.CharField(max_length=255, choices=option)
    prize_title = models.CharField(max_length=255, blank=True, null=True)

    point_as_prize = models.ForeignKey(PointAs_Prize, on_delete=models.CASCADE, blank=True, null=True) # not necessary
    product_as_prize = models.ForeignKey(SponsoredProductForPrize, on_delete=models.CASCADE, blank=True, null=True)
    prize_point_amount = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return self.segment.name + " || " + str(self.segment_no)

    def save(self, *args, **kwargs):
        self.segment_no = self.segment_no + 1
        super().save(*args, **kwargs)

# applicable rules/regulations for prize winner
class ApplicableRulesForWinner(models.Model):
    user = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    product = models.OneToOneField(SponsoredProductForPrize, on_delete=models.CASCADE, blank=True, null=True)
    applicable_rules = models.TextField()

    def __str__(self):
        return self.product.product.title


# model for saving total number of times played the game
class TotalNumOfTimesPlayed(models.Model):
    num_of_times_played = models.IntegerField(default=0)

    def __str__(self):
        return str(self.num_of_times_played)


# terms and policies for game
class GameTermsPolicies(models.Model):
    terms = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.terms


