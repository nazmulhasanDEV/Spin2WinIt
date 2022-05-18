from django.db import models
from user.models import Account, UserProfilePicture
from product.models import *
from django.utils.crypto import get_random_string


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


