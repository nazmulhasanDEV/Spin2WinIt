from django.db import models
from user.models import *
from adminPanel.models import ProductCategory, ProductSubCategory
from django.core.validators import MinValueValidator, MaxValueValidator


class ProductImg(models.Model):
    product_id = models.CharField(max_length=255, blank=True, null=True)
    product_type = models.CharField(max_length=5, blank=True, null=True)
    img = models.ImageField(upload_to='productImg', blank=True, null=True)
    img_link = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

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

    class Meta:
        ordering = ['-pk']

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

    sponsor_status = models.CharField(default='No', max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['-pk']

    objects = models.Manager()
    wspObjects = woocmrcePrdcts()
    mcpObjects = customPrducts()

    def __str__(self):
        return self.title


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
    order_status = models.CharField(max_length=255, choices=option, blank=True, null=True)

    def __str__(self):
        return "Title: " + self.product.title + " || " + str(self.user.email)

# order
class OrderList(models.Model):

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
    items = models.ManyToManyField(OrderedItem, blank=True)
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


# banner section
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




