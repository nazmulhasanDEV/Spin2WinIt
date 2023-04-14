from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    re_path(r'^fetch-shopify-products/$', views.getProductFromShopify, name="getShopifyProducts"),
    re_path(r'^shopify-products/$', views.shopify_products, name="shopifyProducts"),
    re_path(r'^remove-shopify-products/(?P<pk>\d+)/$', views.removeItemFromShopifyStore, name="removeItemFromShopifyStore"),

    re_path(r'^create-order/$', views.createOrder, name="createOrder"),
]

