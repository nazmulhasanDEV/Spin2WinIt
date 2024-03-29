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



SHOPIFY_PASSWORD = '2023@Spin'
SHOPIFY_SHARED_SECRET = '3578de673ff5a90197a34553aade4e15'
SHOPIFY_STORE_URL = 'https://mywybuy.myshopify.com/'


@login_required(login_url='/ap/register/updated')
def getProductFromShopify(request):
    url = 'https://mywybuy.myshopify.com/admin/api/2023-01/products.json/'
    token = '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'
    product_request = requests.get(url, headers={'X-Shopify-Access-Token': token})
    products = json.loads(product_request.text)
    if len(products['products']) > 0:
        for product in products['products']:
            if len(ProductList.shopifyProducts.filter(product_id=product['id'])) <= 0:
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
                        vairant_id=variant['id'],
                        product_id=variant['product_id'],
                        variant_title=variant['title'],
                        variant_price=variant['price'],
                        variant_sku=variant['sku'],
                        position=variant['position'],
                        inventory_policy=variant['inventory_policy'] or '',
                        compare_at_price=variant['compare_at_price'] or '',
                        fulfillment_service=variant['fulfillment_service'] or '',
                        inventory_management=variant['inventory_management'] or '',
                        created_at=variant['created_at'],
                        updated_at=variant['updated_at'],
                        taxable=variant['taxable'] or '',
                        barcode=variant['barcode'] or '',
                        grams=variant['grams'] or '',
                        weight=variant['weight'] or '',
                        weight_unit=variant['weight_unit'] or '',
                        inventory_item_id=variant['inventory_item_id'] or '',
                        inventory_quantity=variant['inventory_quantity'] or '',
                        old_inventory_quantity=variant['old_inventory_quantity'] or '',
                        requires_shipping=variant['requires_shipping'] or '',
                        option1=variant['option1'] or '',
                        option2=variant['option2'] or '',
                        option3=variant['option3'] or '',
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


def createOrder(request):
    # Endpoint URL for creating an order
    url = f"{SHOPIFY_STORE_URL}/admin/api/2023-01/orders.json"
    token = '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'
    api_key = '71e9cbc768a8d132d0b1867ee549a080'
    secret_key = '1af8539ed1df8ac05299e9fe767af955'
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': token
    }

    # Request payload for creating the order

    payload = {
        "order": {
            "line_items": [
                {"variant_id": 44454513180982, 'quantity': 1}
            ],
            "customer": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "nazmulhasan747406@gmail.com"
            },
            "shipping_address": {
                "first_name": "John",
                "last_name": "Doe",
                "company": "Shopify",
                "address1": "150 Elgin St",
                "address2": "",
                "city": "Ottawa",
                "province": "Ontario",
                "country": "Canada",
                "zip": "K2P 1L4",
                "phone": "+8801405727627"
            },
            "note": "This is a test order",
            "currency": "CAD"
        }
    }
    # auth = ("71b798511963e2d900a6b751d7b37c72", "3578de673ff5a90197a34553aade4e15"),

    # Make the POST request to create the order
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    return redirect('shopifyProducts')





# def createOrder(request):
#     # Build the API URL for creating draft orders
#     SHOPIFY_PASSWORD = '2023@Spin'
#     SHOPIFY_SHARED_SECRET = '3578de673ff5a90197a34553aade4e15'
#     SHOPIFY_SECRET_KEY = '71b798511963e2d900a6b751d7b37c72'
#     SHOPIFY_STORE_URL = 'https://mywybuy.myshopify.com/'
#     # Endpoint URL for creating an order
#     url = f"{SHOPIFY_STORE_URL}/admin/api/2023-01/orders.json"
#     token = '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'
#     # Set the headers for the API request
#     headers = {
#         "Content-Type": "application/json",
#         'X-Shopify-Access-Token': token
#     }
#
#     # Request payload for creating the order
#     payload = {
#         'draft_order': {
#             'email': 'customer@example.com',  # Customer email address
#             'billing_address': {
#                 'address1': '123 Main St',
#                 'city': 'New York',
#                 'province': 'NY',
#                 'country': 'United States',
#                 'zip': '10001'
#             },
#             'line_items': [
#                 {"variant_id": 44454513180982, 'quantity': 1}
#             ]
#         }
#     }
#
#     # Make the POST request to create the order
#     response = requests.post(url, json=payload, headers=headers)
#     print(response)
#
#     return redirect('shopifyProducts')


def createOrder1(request):
    SHOPIFY_API_KEY = '71b798511963e2d900a6b751d7b37c72'
    SHOPIFY_PASSWORD = '2023@Spin'
    admin_access_token = "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"
    storefront_token = '3f1d466709c730749ea96fcc2b78d996'
    # Set the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": admin_access_token
    }
    # Define the products to add to the draft order
    products = [
        {"variant_id": 44454513148214, "quantity": 2},
        {"variant_id": 44454513180982, "quantity": 1}
    ]

    # Set up authentication and endpoint URL
    auth = ("API_KEY", "API_PASSWORD")
    url = f"https://{SHOPIFY_STORE_URL}/admin/api/2021-04/shipments.json"

    # Set up request payload with order ID, shipping address, and line items
    payload = {
        "shipment": {
            "order_id": 5341328179510,
            "shipping_address": {
                "first_name": "John",
                "last_name": "Doe",
                "address1": "123 Main St",
                "city": "Anytown",
                "province_code": "ON",
                "zip": "L6Y 5S5",
                "country_code": "CA"
            },
            "line_items": [
                {
                    "variant_id": 44454513148214,
                    "quantity": 1
                }
            ]
        }
    }

    # Send the POST request
    response = requests.get(url, json=payload, headers=headers)
    print(response)

    # Get the shipping cost from the response JSON
    # shipping_cost = response.json()["shipment"]["shipping_rates"][0]["price"]

    # print("Shipping cost:", shipping_cost)

    return redirect('shopifyProducts')


@login_required(login_url='/ap/register/updated')
def addSponsoredProduct(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    product = get_object_or_404(ProductList, pk=pk)

    if product.sponsor_status == 'No' or product.sponsor_status == 'no':
        product.sponsor_status = 'Yes'
        product.save()

        # adding to sponsored product list
        addToSponsoredProductList = SponsoredProductForPrize(product=product, status=False)
        addToSponsoredProductList.save()

        messages.success(request, "Product has been added to sponsored product list. Please activate to add in game segments")
        return redirect('shopifyProducts')

    return redirect('shopifyProducts')



