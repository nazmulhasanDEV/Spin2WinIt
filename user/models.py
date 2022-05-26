from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.crypto import get_random_string


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, phone_no, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_no=phone_no,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_no, password=None):
        user = self.create_user(
            email,
            username=username,
            phone_no=phone_no,
            password=password,
        )

        user.is_admin = True
        user.is_a_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    options = (
        ('1', 'Verified'),
        ('0', 'Not Verified'),
    )

    fname = models.CharField(max_length=255, default='')
    lname = models.CharField(max_length=255, default='')
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(verbose_name='username', max_length=50, unique=True)
    phone_no = models.CharField(max_length=255, default='', unique=True)
    nid_no = models.CharField(max_length=255, default='', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False) # shopper
    is_a_staff = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=options, blank=True, null=True, default=0)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_no']

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# user unique refer code
class ReferalCode(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(default='', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email + " || " + self.code

# generating unique referal code while user creating
def createUniqueReferalCode(sender, instance, created, **kwargs):
    if created:
        if ReferalCode.objects.filter(user=instance).count() <= 0:
            create_referal_code = ReferalCode.objects.create(user=instance, code=get_random_string(10))
post_save.connect(createUniqueReferalCode, sender=Account)


# model for giving permission/checking permission for reset password or mail
class ResetPermissionStatus(models.Model):
    option = (
        ('1', 'Permitted'),
        ('0', 'Not Permitted')
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='0', choices=option)

    def __str__(self):
        return self.user.email + " || " + self.status

# user profile picture section
class UserProfilePicture(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='profile_picture')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


# user mail invitations
class UserMailInvitations(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True)
    mail_to = models.CharField(max_length=255, blank=True)
    msg = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email + " || " + self.mail_to


# verification code model(not necessary)
class VerificationCode(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    user_email = models.CharField(max_length=255, default='', blank=True, null=True)
    code = models.CharField(max_length=6, default='')
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.user_email) + '|| Code: ' + self.code


# user default billing informations
class DefaultBillingInfo(models.Model):
    info_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, blank=True, null=True)
    fname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    town_or_city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)

# user billing informations(newly added on checkout page)
class BillingInfo(models.Model):

    info_id = models.CharField(max_length=255, blank=True, null=True)

    use_defalut_address = models.BooleanField(default=False, blank=True, null=True)
    default_billingAddress = models.ForeignKey(DefaultBillingInfo, on_delete=models.CASCADE, blank=True, null=True)

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, blank=True, null=True)
    fname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    town_or_city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)


# user default billing informations
class DefalutShippingInfo(models.Model):
    info_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    fname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    appartment = models.TextField(blank=True, null=True)
    town_or_city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)

# user billing informations(newly added on checkout page)
class ShippingInfo(models.Model):
    info_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    use_deflt_address = models.BooleanField(default=False, blank=True, null=True)
    default_shipping_address = models.ForeignKey(DefalutShippingInfo, on_delete=models.CASCADE, blank=True, null=True)

    fname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    appartment = models.TextField(blank=True, null=True)
    town_or_city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)


# disclaimer model
class DisclaimerAgreeDisagreeIPList(models.Model):
    ip = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.ip

# checkbox captcha for home page
class CheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for shop page
class ShopCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for shop page by category
class CategoryShopCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for product details page
class ProductDetailsCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)


# checkbox captcha for game page
class GameCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for user-profile page
class UsrProfileCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for buy winning chance page
class BuyWinningChanceBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for cart page
class CartCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for checkout page
class CheckoutCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for contact us page
class ContactUsCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for payment page for purchasing winning chance
class PaymentWinningChnceCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for payment page for product purchasing
class ProductPurchaseCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for payment success page after purchasing product
class ProdctPaymntSccssCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for wishlisht page
class WishlistCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for purchase credit page
class PurchaseCreditCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for credit purchasing payment page
class CreditPurchasePaymntCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for credit purchase success msg page
class CreditPurchaseSuccessCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# checkbox captcha for succcess msg of winning chance purchase
class WnChancePurchaseSccMsgCheckBoxCaptcha(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)

# invisible captcha
class InvisibleFeedbackCaptcha(models.Model):

    option = (
        ('g', "Good"),
        ('b', "Better"),
        ('a', "Awesome"),
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255, choices=option, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user.email)
