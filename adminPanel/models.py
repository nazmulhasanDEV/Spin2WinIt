from django.db import models
from user.models import *
from product.models import *
import requests



# product categories model
class ProductCategory(models.Model):
    name = models.CharField(default='', max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.name

# product sub-categories
class ProductSubCategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.name + ' || ' + str(self.category.name)

# membership type model**********************
class MemberShipRank(models.Model):
    rank_id = models.CharField(default='', max_length=20, blank=True, null=True)
    title = models.CharField(default='', max_length=20)
    total_earnings = models.FloatField(default=0.0, blank=True, null=True)
    number_of_prodct_need_to_sell = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# membership status
class SellerMembershipStatus(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    membership_rank = models.ForeignKey(MemberShipRank, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + " || " + self.membership_rank.title


class SiteLogo(models.Model):
    logo = models.ImageField(upload_to='logo')
    created = models.DateTimeField(auto_now_add=True)

# top footer
class FreeDelivery(models.Model):
    des = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.des

class SafePayment(models.Model):
    des = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.des

class ShopWithConfidence(models.Model):
    des = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.des

class HelpCenter(models.Model):
    des = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.des

# about us model
class AboutUs(models.Model):
    about_us = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.about_us


# subscriber list
class SubscriberList(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# contact us
class ContactUs(models.Model):
    short_qoute = models.TextField()
    address_line_one = models.CharField(max_length=255, default='')
    address_line_two = models.CharField(max_length=255, default='', blank=True, null=True)
    mobile = models.CharField(max_length=50, default='')
    hotline = models.CharField(max_length=50, default='', blank=True, null=True)
    email_one = models.CharField(max_length=50, default='')
    email_two = models.CharField(max_length=50, default='', blank=True, null=True)

    def __str__(self):
        return self.mobile


# beta test terms and conditions
class BetaTestTermsConditions(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# members policy
class MembersPolicy(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
class ShopperPolicy(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


# delivery policy
class DeliveryPolicy(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# return policy
class ReturnPolicy(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# refund policy
class RefundPolicy(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# security policy
class SecurityPolicy(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# terms-conditions policy
class TermsConditions(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# privacy policy
class PrivacyPolicy(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# cookie policy
class CookiePolicy(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# customer messages
class CustomerMessageList(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subj = models.CharField(max_length=255)
    msg = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " || " + self.msg

# visitors/shopper list/information
def get_location(ip):
    response = requests.get(f'https://ipapi.co/{ip}/json/').json()
    location_data = {
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "country_code": response.get("country_code"),
        "postal": response.get("postal"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude"),
        "timezone": response.get("timezone"),
    }
    return location_data

class VisitorInfo(models.Model):
    visitor_ip = models.CharField(max_length=255, blank=True)
    visitors_country = models.CharField(max_length=50, blank=True, null=True)
    country_code = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    visited = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.visitor_ip

    def save(self, *args, **kwargs):
        details_of_crnt_ip = get_location(self.visitor_ip)

        self.visitors_country = details_of_crnt_ip['country']
        self.country_code = details_of_crnt_ip['country_code']
        self.latitude = details_of_crnt_ip['postal']
        self.longitude = details_of_crnt_ip['latitude']
        self.postal_code = details_of_crnt_ip['postal']
        self.timezone = details_of_crnt_ip['longitude']
        super(VisitorInfo, self).save(*args, **kwargs)

# total visitors
class TotalNumVisitor(models.Model):
    num_of_visitor = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return str(self.num_of_visitor)

# package name section starts
class PackageNameList(models.Model):
    name = models.CharField(default='', max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

class PackageOptions(models.Model):
    option = models.CharField(default='', max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.option



# how it works section starts here ******************************************

# how "spinit2win" works
class HowSpinIt2WinWorks(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
