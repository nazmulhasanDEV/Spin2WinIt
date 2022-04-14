from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^fe/index/$', views.front_index, name="frontEndIndex"),
    re_path(r'^$', views.front_home, name='frontEndHome'),
    re_path(r'^fe/login/register/$', views.front_loginRegister, name='frontEndLoginRegister'),
    re_path(r'^fe/login/user/$', views.front_loginUser, name="frontEndLoginUser"),

    # forgot password
    re_path(r'^fe/provide/email/to/reset/password/$', views.front_give_email_to_reset_pass, name='frontGiveEmailResetPassword'),
    re_path(r'^fe/reset/password/(?P<username>\w+)/$', views.front_reset_password, name='frontResetPassword'),

    # shop by category
    re_path(r'^fe/shop/(?P<pk>\d+)/$', views.front_shop, name='frontShop'),
    # product details
    re_path(r'^fe/product/details/(?P<product_id>[-\w]+)/$', views.front_productDetails, name='frontEndProductDetails'),

    # user profile section **************************
    re_path(r'^fe/buyer/user/profile/(?P<username>\w+)/$', views.front_user_profile, name='frontEndUserProfile'),
    re_path(r'^fe/logout/user/$', views.front_logoutUser, name='frontEndLogoutUser'),
    re_path(r'^fe/update/profile/pircture/$', views.front_updateProfile_picture, name='frontUpdateProfilePic'),
    re_path(r'^fe/update/user/username/$', views.front_update_username, name='frontUpdateUserUsername'),
    re_path(r'^fe/update/internal/password/$', views.front_update_internal_password, name='frontUpdateInternalPassword'),

    # product cart, wishlist section
    re_path(r'^fe/add/to/cart/(?P<product_id>[-\w]+)/$', views.front_add_to_cart, name='frontAddToCart'),
    re_path(r'^fe/cart/items/(?P<username>[-\w]+)/$', views.front_cart_items_list, name='frontCartItemsList'),
    re_path(r'^fe/cart/checkout/(?P<username>[-\w]+)/$', views.front_checkout, name='frontEndCheckOut'),
    re_path(r'^fe/confirm/order/(?P<username>[-\w]+)/$', views.front_confirm_order, name='frontConfirmOrder'),
    re_path(r'^fe/complete/payment/(?P<username>[-\w]+)/(?P<order_id>[-\w]+)/$', views.front_complete_payment, name='frontCompletePayment'),
    re_path(r'^fe/remove/item/from/mini/cart/(?P<pk>\d+)/$', views.front_remove_item_from_mini_cart, name='frontRemovItemFromMiniCart'),

    # buy now
    re_path(r'^fe/buy/now/(?P<product_id>[-\w]+)/$', views.front_buy_now, name='frontBuyNow'),

    # leave review
    re_path(r'^fe/leave/review/(?P<product_id>[-\w]+)/$', views.front_leave_product_review, name="frontLeaveProductReview"),

    # wishlist
    re_path(r'^fe/add/to/wishlist/(?P<product_id>[-\w]+)/$', views.front_add_to_wishlist, name='frontAddToWishlist'),
    re_path(r'^fe/wishlist/(?P<username>[-\w]+)/$', views.front_wishlist, name='frontWishlist'),
    re_path(r'^fe/remove/item/wishlist/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.front_remove_item_from_wishlist, name='frontRemoveItemFromWishlist'),

    # gameing urls
    re_path(r'^fe/game/$', views.front_game, name='frontGame'),
    re_path(r'^fe/buy/winning/chance/$', views.front_buy_winning_chance, name='frontBuyWinningChance'),
    re_path(r'^fe/pay/for/game/purchasing/chance/$', views.front_pay_for_purchasing_wnning_chance, name='frontPayForPurchasingGame'),
    re_path(r'^fe/payment/successfull/msg/(?P<username>[-\w]+)/$', views.front_payment_successfull_msg, name='frontPaymentSuccessfullmsg'),

    # policy section
    re_path(r'^fe/refund/policy/$', views.front_refund_policy, name='frontRefundPolicy'),
    re_path(r'^fe/return/policy/$', views.front_return_policy, name='frontReturnPolicy'),
    re_path(r'^fe/security/policy/$', views.front_security_policy, name='frontSecurityPolicy'),
    re_path(r'^fe/delivery/policy/$', views.front_delivery_policy, name='frontDeliveryPolicy'),

    # company
    re_path(r'^fe/about/us/$', views.front_about_us, name='frontAboutUs'),
    re_path(r'^fe/cookie/policy/$', views.front_cookie_policy, name='frontCookiePolicy'),
    re_path(r'^fe/terms/condition/$', views.front_terms_conditions, name='frontTermsCondition'),
    re_path(r'^fe/privacy/policy/$', views.front_privacy_policy, name='frontPrivacyPolicy'),
]
