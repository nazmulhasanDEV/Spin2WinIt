from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^seller/dashboard/index/$', views.seller_dashboard_index, name='sellerDashboardIndex'),
    re_path(r'^seller/dashboard/(?P<username>\w+)/$', views.seller_dashboard_home, name='sellerDashboardHome'),

    # product section
    re_path(r'^seller/add/product/$', views.seller_add_product, name='sellerAddProduct'),
    re_path(r'^seller/custom/product/list/$', views.seller_custom_product_list, name='sellerCustomProductList'),
    re_path(r'^seller/custom/product/update/(?P<pk>\d+)/$', views.seller_update_custom_product, name='sellerCustomProductUpdate'),
    re_path(r'^seller/custom/product/details/(?P<pk>\d+)/(?P<product_id>[-\w]+)/$', views.seller_custom_product_detail, name='sellerCustomProductDetails'),
    re_path(r'^seller/del/custom/product/(?P<pk>\d+)/(?P<product_id>[-\w]+)/$', views.seller_del_custom_product, name='sellerDelCustomProduct'),

    # all packages part starts*****************************
    re_path(r'^seller/all/the/packages/$', views.seller_all_packages, name='sellerAllThePackages'),
    re_path(r'^seller/pay/for/package/purchase/(?P<package_id>[-\w]+)/$', views.seller_payforPurchasingPackage, name='sellerPayForPackagePurchasing'),
    re_path(r'^seller/package/payment/success/(?P<username>[-\w]+)/$', views.seller_payment_success_msg, name='sellerPackagePaymentSuccess'),
    re_path(r'^seller/package/details/(?P<package_id>[-\w]+)/$', views.seller_package_details, name='sellerPackageDetails'),

    # collection
    re_path(r'^seller/collect/product/$', views.seller_collect_product, name='sellerCollectProduct'),
    re_path(r'^seller/add/product/to/collections/(?P<product_id>[-\w]+)/$', views.seller_addProductToCollections, name='seller_addProductToCollections'),
    re_path(r'^seller/product/collection/list/$', views.seller_productCollections, name='sellerProductCollectionList'),

    # profile
    re_path(r'^seller/profile/setting/(?P<username>[-\w]+)/$', views.seller_profile_setting, name='sellerProfileSetting'),
    re_path(r'^seller/upate/profile/pic/$', views.seller_update_profile_pic, name='sellerUpdateSellerProfilePic'),
    re_path(r'^seller/update/full/name/$', views.seller_update_full_name, name='sellerUpdateFullName'),
    re_path(r'^seller/update/user/password/$', views.seller_update_user_password, name='sellerUpdateUserPassword'),
]

