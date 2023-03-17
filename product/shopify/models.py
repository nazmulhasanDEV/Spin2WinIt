from django.db import models
from user.models import *
from adminPanel.models import ProductCategory, ProductSubCategory, MemberShipRank
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ProductOption(models.Model):
    option_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    position = models.IntegerField(default=0)
    values = models.TextField()

class ShopifyProductVariant(models.Model):
    vairant_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    variant_title = models.CharField(max_length=255)
    variant_price = models.CharField(max_length=255)
    variant_sku = models.CharField(max_length=255)
    position = models.IntegerField(default=0)
    inventory_policy = models.CharField(max_length=255)
    compare_at_price = models.CharField(max_length=255)
    fulfillment_service = models.CharField(max_length=255)
    inventory_management = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)
    updated_at = models.CharField(max_length=255)
    taxable = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    grams = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    weight_unit = models.CharField(max_length=255)
    inventory_item_id = models.CharField(max_length=255)
    inventory_quantity = models.CharField(max_length=255)
    old_inventory_quantity = models.CharField(max_length=255)
    requires_shipping = models.CharField(max_length=255)
    option1 = models.CharField(default='white', max_length=255)
    option2 = models.CharField(default='', max_length=255)
    option3 = models.CharField(default='', max_length=255)