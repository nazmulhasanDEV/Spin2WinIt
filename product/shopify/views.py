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


import requests

def create_draft_order(products):
    # Build the API URL for creating draft orders
    url = f"{SHOPIFY_STORE_URL}/admin/api/2021-07/draft_orders.json"
    token = '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'
    # Set the headers for the API request
    headers = {
        "Content-Type": "application/json",
        'X-Shopify-Access-Token': token
    }

    # Build the payload for the API request
    payload = {
        "draft_order": {
            "line_items": [

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

    # Add the line items to the payload
    for product in products:
        line_item = {
            "variant_id": product["variant_id"],
            "quantity": product["quantity"]
        }
        payload["draft_order"]["line_items"].append(line_item)

    # Send the API request to create the draft order
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code
    if response.status_code == 201:
        # Draft order created successfully
        draft_order_id = response.json()["draft_order"]["id"]
        # print(draft_order_id)

        return draft_order_id
    else:
        # Error creating draft order
        error_message = response.json()["errors"]
        raise Exception(error_message)


def createOrder(request):
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

# def createOrder(request):
#     shop = shopify.Order()
#
#     url = 'https://mywybuy.myshopify.com//admin/api/2023-01/orders.json/'
#     token = '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'
#     data = {
#         "order": {
#             "line_items": [
#                 {
#                     "variant_id": 44454513180982,
#                     "quantity": 1
#                 }
#             ],
#             "tax_lines": [
#                 {
#                     "price": 13.5,
#                     "rate": 0.06,
#                     "title": "State tax"
#                 }
#             ]
#         }
#     }
#     order_request = requests.post(url, json=data, headers={'X-Shopify-Access-Token': token})
#     print(order_request)
#
#     return redirect('shopifyProducts')










