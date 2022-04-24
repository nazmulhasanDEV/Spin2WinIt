from django.db import models

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
