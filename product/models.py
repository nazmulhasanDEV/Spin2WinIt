from django.db import models
from user.models import *
from adminPanel.models import ProductCategory, ProductSubCategory, MemberShipRank
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ShippingClass(models.Model):
    classID = models.CharField(default='', max_length=255, blank=True, null=True)
    name = models.CharField(default='', max_length=255)
    cost_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name + " Cost: " + str(self.cost_rate)

class ProductWeightCriteria(models.Model):
    criteria_id = models.CharField(max_length=255, blank=True, null=True)
    min_weight = models.FloatField(default=0)
    max_weight = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.min_weight) + "-" + str(self.max_weight)


class ProductImg(models.Model):
    product_id = models.CharField(max_length=255, blank=True, null=True)
    product_type = models.CharField(max_length=5, blank=True, null=True)
    img = models.ImageField(upload_to='productImg', blank=True, null=True)
    img_link = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.product_id


# woocommerce product list
class WoocommerceProductList(models.Model):
    product_id = models.CharField(max_length=255, default='')
    product_img = models.ManyToManyField(ProductImg, blank=True)
    name = models.TextField()
    slug = models.TextField()
    description = models.TextField()
    price = models.CharField(max_length=255, default='')
    regular_price = models.CharField(max_length=255, blank=True, null=True)
    total_sales = models.CharField(max_length=255, blank=True, null=True)

    cat_id = models.CharField(max_length=255)
    cat_name = models.CharField(max_length=255)
    subcat_id = models.CharField(max_length=255, blank=True, null=True)
    subcat_name = models.CharField(max_length=255, blank=True, null=True)
    stock_status = models.CharField(max_length=255)
    avrg_rating = models.CharField(max_length=255, blank=True, null=True)
    rating_count = models.CharField(max_length=255, blank=True, null=True)
    sponsr_as_prize = models.BooleanField(default=False, blank=True, null=True)

    product_weight = models.CharField(default='', max_length=50, blank=True, null=True)
    product_length = models.CharField(default='', max_length=50, blank=True, null=True)
    product_width = models.CharField(default='', max_length=50, blank=True, null=True)
    product_height = models.CharField(default='', max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name[0:10] + " || " + str(self.id)


class ProductList(models.Model):

    class woocmrcePrdcts(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(product_type='wsp')

    class customPrducts(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(product_type='mcp')

    productType = (
        ('wsp', 'Woocommerce store product'), # wsp refers to "woocomerce store products"
        ('mcp', 'Custom Product'), # mcp refers to "My custom products"
    )
    product_type = models.CharField(max_length=255, choices=productType, blank=True, null=True)
    product_id = models.CharField(default='id', max_length=255, blank=True, null=True)
    slug = models.TextField(default='slug', blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True, null=True)
    cat_id = models.CharField(default='id', max_length=255, blank=True, null=True)
    cat_name = models.CharField(default='cat_name', max_length=255, blank=True, null=True)

    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, blank=True, null=True)
    subcat_id = models.CharField(default='id', max_length=255, blank=True, null=True)
    subcat_name = models.CharField(default='subcat_name', max_length=255, blank=True, null=True)

    title = models.TextField(default="title", blank=True, null=True)
    brand_name = models.CharField(default='brand_name', max_length=255, blank=True, null=True)
    old_price = models.FloatField(default=0, blank=True, null=True) # for custom product
    new_price = models.FloatField(default=0, blank=True, null=True) # for custom product
    short_des = models.TextField(default='Description', blank=True, null=True)
    details = models.TextField(default='Details', blank=True, null=True)

    product_thumbnail = models.ImageField(upload_to="product_thumbnail_img", blank=True, null=True)
    productImg = models.ManyToManyField(ProductImg, blank=True)

    policy_followed = models.CharField(default='Not selected', max_length=255, blank=True, null=True)

    use_case = models.TextField(default='Not added', blank=True, null=True)
    benefits = models.TextField(default='Not added', blank=True, null=True)
    security_policy = models.TextField(default='Not added', blank=True, null=True)
    return_policy = models.TextField(default='Not added', blank=True, null=True)
    delivery_policy = models.TextField(default='Not added', blank=True, null=True)
    refund_policy = models.TextField(default='Not added', blank=True, null=True)

    store_name = models.CharField(default='Not added', max_length=255, blank=True, null=True)
    store_link = models.CharField(default='Not added', max_length=255, blank=True, null=True)
    about_store = models.TextField(default='', blank=True, null=True)

    total_sold = models.IntegerField(default=0, blank=True, null=True)
    in_stock = models.CharField(default='0', max_length=255, blank=True, null=True)

    avrg_rating = models.CharField(default='0', max_length=255, blank=True, null=True)
    rating_count = models.CharField(default='0', max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    regular_price = models.CharField(max_length=255, blank=True, null=True)

    sponsr_as_prize = models.BooleanField(default=False, blank=True, null=True) # not used/not needed

    product_weight = models.FloatField(default=0, blank=True, null=True)
    product_length = models.CharField(max_length=50, blank=True, null=True)
    product_width = models.CharField(max_length=50, blank=True, null=True)
    product_height = models.CharField(max_length=50, blank=True, null=True)

    shipping_class = models.ForeignKey(ShippingClass, on_delete=models.PROTECT, blank=True, null=True)

    sponsor_status = models.CharField(default='No', max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['-pk']

    objects = models.Manager()
    wspObjects = woocmrcePrdcts()
    mcpObjects = customPrducts()

    def __str__(self):
        return self.title



# offered product items  together according to membership rank
class OfferedProductItemsByMembershipRank(models.Model):
    membership_rank = models.ForeignKey(MemberShipRank, on_delete=models.CASCADE)
    product_cat = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, blank=True, null=True)
    product = models.ManyToManyField(ProductList, blank=True)
    discount_amount = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.membership_rank.title + " || " + str(self.discount_amount)

# offered product list based on membeship rank
class OfferedSingleProductBasedOnMembershipRank(models.Model):
    membership_rank = models.ForeignKey(MemberShipRank, on_delete=models.CASCADE)
    product_cat = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, blank=True, null=True)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE, blank=True, null=True)
    discount_amount = models.IntegerField(default=0, blank=True)
    offered_price = models.FloatField(default=0.0, blank=True)

    def save(self, *args, **kwargs):
        if self.product.product_type == 'wsp' and self.discount_amount > 0:
            self.offered_price = round((float(self.product.price) * self.discount_amount) / 100, 2)
            super(OfferedSingleProductBasedOnMembershipRank, self).save(*args, **kwargs)
        elif self.product.product_type == 'wsp' and self.discount_amount <= 0:
            self.offered_price = round(float(self.product.price), 2)
            super(OfferedSingleProductBasedOnMembershipRank, self).save(*args, **kwargs)
        else:
            self.offered_price = round((self.product.new_price) / 100, 2)
            super(OfferedSingleProductBasedOnMembershipRank, self).save(*args, **kwargs)

    def __str__(self):
        return self.membership_rank.title + " || " + self.product.title + " || " + str(self.discount_amount)


class ProductRating(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    rating_val = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(default='Comment', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_id + " || " + str(self.rating_val)

class ProductDiscount(models.Model):
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    discount_amount = models.CharField(max_length=20, default='')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title + " || " + self.discount_amount



# cart
class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "Title: " + self.product.title+ " || " +str(self.user.email)

    def save(self, *args, **kwargs):
        if self.product.product_type == 'wsp':
            self.total_amount = round(float(self.product.price) * float(self.quantity), 2)
        if self.product.product_type == 'mcp':
            self.total_amount = round(float(self.product.new_price) * float(self.quantity), 2)
        super(Cart, self).save(*args, **kwargs)

# order items
class OrderedItem(models.Model):

    option = (
        ('curnt', 'Current Order'), # curnt == current
        ('prev', 'Previous Order'), # prev == previous
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    total_amount = models.FloatField(blank=True, null=True)
    shipping_cost = models.FloatField(blank=True, null=True)
    order_status = models.CharField(max_length=255, choices=option, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            if self.product.shipping_class.cost_rate:
                self.shipping_cost = self.quantity * (self.product.shipping_class.cost_rate)
                super(OrderedItem, self).save(*args, **kwargs)
        except:
            self.shipping_cost = 0
            super(OrderedItem, self).save(*args, **kwargs)

    def __str__(self):
        return "Title: " + self.product.title + " || " + str(self.user.email)

# order
class OrderList(models.Model):

    option = (
        ('a', 'Approved'),
        ('p', 'Pending'),
        ('c', 'Cancelled'),
    )

    payment_options = (
        ('cod', 'Cash on Delivery'),
    )

    order_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderedItem, blank=True)
    sub_total_amount = models.FloatField(blank=True, null=True)
    total_shipping_cost = models.FloatField(default=0, blank=True, null=True)
    total_amount = models.FloatField(default=0, blank=True, null=True) # shipping cost + sub_total

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

    def save(self, *args, **kwargs):
        self.total_amount = self.sub_total_amount + self.total_shipping_cost
        super(OrderList, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.email)

class ProductPurchasePaymntHistory(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(OrderList, on_delete=models.CASCADE, blank=True, null=True)
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
    created = models.DateTimeField(auto_now_add=True, editable=True, blank=True, null=True)


    def __str__(self):
        return self.user.email + "||" + str(self.paid_amount) + '||' + str(self.created)


# Coupon
class CouponCode(models.Model):
    user = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    coupon_code = models.CharField(max_length=30)
    discount_amnt = models.IntegerField(default=0, blank=True, null=True) # discount in percentage(%)
    status = models.BooleanField(default=False, blank=True, null=True)
    coupon_banner = models.ImageField(upload_to='coupon_banner', blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coupon_code + "||" + str(self.discount_amnt)

# Coupon applied history
class AppliedCouponHistory(models.Model):
    order = models.ForeignKey(OrderList, on_delete=models.CASCADE, blank=True, null=True)
    coupon = models.ForeignKey(CouponCode, on_delete=models.CASCADE, blank=True, null=True)
    discount_got = models.CharField(max_length=24, blank=True, null=True)

    def __str__(self):
        return self.coupon.coupon_code + "||" + self.order.order_id

# wishlist
class WishList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.user.email)

    def save(self, *args, **kwargs):
        if self.product.product_type == 'wsp':
            self.total_amount = float(self.product.price) * self.quantity
        if self.product.product_type == 'mcp':
            self.total_amount = float(self.product.new_price) * self.quantity
        super(WishList, self).save(*args, **kwargs)


# home page main banner section
class BannerList(models.Model):
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    offer_title = models.CharField(max_length=255, blank=True, null=True)
    offer_amount_or_title = models.CharField(max_length=255, blank=True, null=True) # like 20% off or Black Friday
    offer_duration = models.CharField(max_length=255, blank=True, null=True)
    product_title = models.CharField(max_length=255, blank=True, null=True)
    starting_price = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(upload_to='banner', blank=True, null=True)
    product_url = models.CharField(max_length=350, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + " || " + self.product_title

# home page mini top banner
class HomeMiniTopBanner(models.Model):
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='banner', blank=True, null=True)
    url = models.CharField(max_length=350, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.banner_id + "||" + str(self.user.email)


# home page mini bottom banner
class HomeMiniBottomBanner(models.Model):
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='banner', blank=True, null=True)
    url = models.CharField(max_length=350, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.banner_id + "||" + str(self.user.email)




# all product model including woocommercce store and custom product
class AllProductList(models.Model):

    class woocmrcePrdcts(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(product_type='wsp')

    class customPrducts(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(product_type='mcp')

    productType = (
        ('wsp', 'Woocommerce store product'), # wsp refers to "woocomerce store products"
        ('mcp', 'Custom Product'), # mcp refers to "My custom products"
    )
    product_type = models.CharField(max_length=255, choices=productType, blank=True, null=True)
    woocmrce_product = models.ForeignKey(WoocommerceProductList, on_delete=models.PROTECT, blank=True, null=True)
    custom_product = models.ForeignKey(ProductList, on_delete=models.PROTECT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    wspObjects = woocmrcePrdcts()
    mcpObjects = customPrducts()

    def __str__(self):
        return self.product_type