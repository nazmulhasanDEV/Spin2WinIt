import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.models import Account, VerificationCode, UserProfilePicture
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from verification.random_code_gen import rand_num_gen
from verification.email_threadings import EmailThreading
from django.utils import timezone
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from product.models import *
from game.models import *
import uuid
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
import asyncio
import threading
from product.models import *
from config.activate_deactivate_status import activate_status, deactivate_status
from config.custom_functions import delete_obj
from django.db.models import Avg, Sum, Count, Max
import shopify
from pyactiveresource import activeresource as ar
import requests
import json
from .models import ProductOption, ShopifyProductVariant


def getProductFromShopify(request):
    url = 'https://mywybuy.myshopify.com/admin/api/2023-01/products.json/'
    token = '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'
    product_request = requests.get(url, headers={'X-Shopify-Access-Token': token})
    products = json.loads(product_request.text)
    if len(products['products']) > 0:
        for product in products['products']:
            saveToProductList = ProductList.objects.create(
                product_type='shopify_product',
                product_id=product['id'],
                cat_name=product['tags'],
                title=product['title'],
                details=product['body_html'],
            )

            for option in product['options']:
                saveToProductOption = ProductOption.objects.create(
                    option_id=option['id'],
                    product_id=option['product_id'],
                    name=option['name'],
                    position=option['position'],
                    values=option['values']
                )
                saveToProductList.product_options.add(saveToProductOption)
                saveToProductList.save()

            for img in product['images']:
                saveToProductImages = ProductImg.objects.create(
                    img_id=img['id'],
                    product_id=img['product_id'],
                    positions=img['position'],
                    width=img['width'],
                    height=img['height'],
                    img_link=img['src'],
                    created=img['created_at'],
                    updated_at=img['updated_at']
                )
                saveToProductList.productImg.add(saveToProductImages)
                saveToProductList.save()

            for variant in product['variants']:
                saveToVariantList = ShopifyProductVariant.objects.create(
                    vairant_id = variant['id'],
                    product_id = variant['product_id'],
                    variant_title = variant['title'],
                    variant_price = variant['price'],
                    variant_sku = variant['sku'],
                    position = variant['position'],
                    inventory_policy = variant['inventory_policy'] or '',
                    compare_at_price = variant['compare_at_price'] or '',
                    fulfillment_service = variant['fulfillment_service'] or '',
                    inventory_management = variant['inventory_management'] or '',
                    created_at = variant['created_at'],
                    updated_at = variant['updated_at'],
                    taxable = variant['taxable'] or '',
                    barcode = variant['barcode'] or '',
                    grams = variant['grams'] or '',
                    weight = variant['weight'] or '',
                    weight_unit = variant['weight_unit'] or '',
                    inventory_item_id = variant['inventory_item_id'] or '',
                    inventory_quantity = variant['inventory_quantity'] or '',
                    old_inventory_quantity = variant['old_inventory_quantity'] or '',
                    requires_shipping = variant['requires_shipping'] or '',
                    option1 = variant['option1'] or '',
                    option2 = variant['option2'] or '',
                    option3 = variant['option3'] or '',
                )
                saveToProductList.productVariant.add(saveToVariantList)
                saveToProductList.save()

    return redirect('shopifyProducts')

def shopify_products(request):

    products = ProductList.shopifyProducts.all()

    context = {
        'products': products
    }
    return render(request, 'backEnd_superAdmin/shopify/shopify-products.html', context)

def removeItemFromShopifyStore(request, pk):

    try:
        obj = get_object_or_404(ProductList, pk=pk)
        if obj:
            obj.delete()
            messages.success(request, "Successfully deleted")
            return redirect('shopifyProducts')
    except:
        messages.warning(request, "Product can't be deleted")
        return redirect('shopifyProducts')

    return redirect('shopifyProducts')
