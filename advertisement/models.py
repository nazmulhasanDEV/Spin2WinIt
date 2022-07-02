from django.db import models
from user.models import Account
from product.models import ProductList


# ads script setting
class AdsPageName(models.Model):
    page_id = models.CharField(default='', max_length=255, blank=True, null=True)
    name = models.CharField(default='', max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AdsRow(models.Model):

    class HorionotalRectBnrAds(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(allowed_ads_type='hrba')

    class VerticalRectBnrAds(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(allowed_ads_type='vrba')

    class SquareBnrAds(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(allowed_ads_type='sqba')

    allowed_ads_options = (
        ('hrba', 'Horizontal Rectangle Banner Ads'), # vba == 'Horizontal reactangle Banner ads
        ('vrba', 'Vertical Rectangle Banner Ads'), # vba == 'Vertical reactangle Banner ads
        ('sqba', 'Square Banner Ads'), # sqba == "Square Banner Ads"
    )
    row_id = models.CharField(default='', max_length=255, blank=True, null=True)
    page_name = models.ForeignKey(AdsPageName, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=255)
    allowed_ads_type = models.CharField(default='', max_length=255, choices=allowed_ads_options)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    horizontalRectBnrAds = HorionotalRectBnrAds()
    verticalRectBnrAds = VerticalRectBnrAds()
    squareBnrAds = SquareBnrAds()

    def save(self, *args, **kwargs):
        if self.name == 'Row-1':
            self.row_id = 'r1'
            super(AdsRow, self).save(*args, **kwargs)
        if self.name == 'Row-2':
            self.row_id = 'r2'
            super(AdsRow, self).save(*args, **kwargs)
        if self.name == 'Row-3':
            self.row_id = 'r3'
            super(AdsRow, self).save(*args, **kwargs)
        if self.name == 'Row-4':
            self.row_id = 'r4'
            super(AdsRow, self).save(*args, **kwargs)
        if self.name == 'Row-5':
            self.row_id = 'r5'
            super(AdsRow, self).save(*args, **kwargs)
        if self.name == 'Row-6':
            self.row_id = 'r6'
            super(AdsRow, self).save(*args, **kwargs)


    def __str__(self):
        return self.page_name.name + ' || ' + self.name + " || " + self.allowed_ads_type

class AdsColPerRow(models.Model):
    col_id = models.CharField(default='', max_length=255, blank=True, null=True)
    row = models.ForeignKey(AdsRow, on_delete=models.CASCADE)
    col_name = models.CharField(default='', max_length=255)
    ads_script = models.TextField(default='', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if 'Column-1' in self.col_name:
            self.col_id = 'c1'
            super(AdsColPerRow, self).save(*args, **kwargs)
        if 'Column-2' in self.col_name:
            self.col_id = 'c2'
            super(AdsColPerRow, self).save(*args, **kwargs)
        if 'Column-3' in self.col_name:
            self.col_id = 'c3'
            super(AdsColPerRow, self).save(*args, **kwargs)
        if 'Column-4' in self.col_name:
            self.col_id = 'c4'
            super(AdsColPerRow, self).save(*args, **kwargs)
        if 'Column-5' in self.col_name:
            self.col_id = 'c5'
            super(AdsColPerRow, self).save(*args, **kwargs)
        if 'Column-6' in self.col_name:
            self.col_id = 'c6'
            super(AdsColPerRow, self).save(*args, **kwargs)
        if 'Column-7' in self.col_name:
            self.col_id = 'c7'
            super(AdsColPerRow, self).save(*args, **kwargs)

    def __str__(self):
        return self.row.page_name.name + "||" + self.row.name + "||" + self.col_name

class AdsScript(models.Model):
    page = models.ForeignKey(AdsPageName, on_delete=models.CASCADE)
    row = models.ForeignKey(AdsRow, on_delete=models.CASCADE)
    col = models.ForeignKey(AdsColPerRow, on_delete=models.CASCADE)
    adsScript = models.TextField(default='')

    def __str__(self):
        return self.page.name + '||' + self.row.name + '||' + self.col.col_name + '||' + self.adsScript



# banner at product details page
class BannerProdDetail(models.Model):
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    img = models.ImageField(upload_to='Product_details_pg_bnr')
    link = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.banner_id

# banner at shop page by category
class ShopPageBanner(models.Model):
    banner_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    img = models.ImageField(upload_to='shopPageBanner')
    link = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.banner_id

# banner/product advertisement on user profile page
class UserProfileAds(models.Model):

    ADS_TYPE = (
        ('banner', 'Banner'),
        ('product', 'Product'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    ads_type = models.CharField(choices=ADS_TYPE, max_length=25)
    banner_img = models.ImageField(blank=True, null=True, upload_to='user_profile_ads_bnnr')
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.ads_type


