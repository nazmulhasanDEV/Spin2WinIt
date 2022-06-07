from django.contrib import admin
from django.urls import path, include, re_path
from . import views
import uuid

urlpatterns = [

    re_path(r'^fe/get/user/ip/$', views.get_User_ip, name='frontGetUserIp'),

    re_path(r'^fe/index/$', views.front_index, name="frontEndIndex"),
    re_path(r'^$', views.front_home, name='frontEndHome'),
    re_path(r'^fe/all/available/packges/$', views.front_all_packages, name='frontAllAvailabePackages'),

    # checkbox captcha solving and bonus
    re_path(r'^fe/checkbox/captcha/bonus/$', views.front_checkBoxCaptchaBonus, name='frontCheckBoxCaptchaBonus'),
    re_path(r'^fe/shop/page/checkbox/captcha/bonus/$', views.front_ShopCheckBoxCaptcha, name='frontShopCheckBoxCaptchaBonus'),
    re_path(r'^fe/shop/page/by/category/checkbox/captcha/bonus/$', views.front_CategoryShopCheckBoxCaptcha, name='frontCategoryShopCheckBoxCaptchaBonus'),
    re_path(r'^fe/product/details/checkbox/captcha/bonus/$', views.front_ProductDetailsCheckBoxCaptcha, name='frontProductDetailsCheckBoxCaptchaBonus'),

    re_path(r'^fe/game/page/checkbox/captcha/bonus/$', views.front_GameCheckBoxCaptcha, name='frontGamePageCheckBoxCaptchaBonus'),
    re_path(r'^fe/user/profile/page/checkbox/captcha/bonus/$', views.front_UsrProfileCheckBoxCaptcha, name='frontGUsrProfilePgCheckBoxCaptchaBonus'),
    re_path(r'^fe/purchase/winning/chance/page/checkbox/captcha/bonus/$', views.front_BuyWinningChanceBoxCaptcha, name='frontPurchaseWinningChncePgCheckBoxCaptchaBonus'),
    re_path(r'^fe/cart/page/checkbox/captcha/bonus/$', views.front_CartCheckBoxCaptcha, name='frontCartPgCheckBoxCaptchaBonus'),

    re_path(r'^fe/checkout/page/checkbox/captcha/bonus/$', views.front_CheckoutCheckBoxCaptcha, name='frontCheckOutPgCheckBoxCaptchaBonus'),
    re_path(r'^fe/contact/us/page/checkbox/captcha/bonus/$', views.front_ContactUsCheckBoxCaptcha, name='frontContactUsPgCheckBoxCaptchaBonus'),
    re_path(r'^fe/payment/page/purchasing/winning/chance/checkbox/captcha/bonus/$', views.front_PaymentWinningChnceCheckBoxCaptcha, name='frontPymntPgPrchasingWinningChnceCheckBoxCaptchaBonus'),
    re_path(r'^fe/product/purchasing/payment/checkbox/captcha/bonus/$', views.front_ProductPurchaseCheckBoxCaptcha, name='frontPymntPgProdctPurchaseCheckBoxCaptchaBonus'),

    re_path(r'^fe/product/purchasing/payment/success/checkbox/captcha/bonus/$', views.front_ProdctPaymntSccssCheckBoxCaptcha, name='frontPymntPgProdctPurchaseSuccessCheckBoxCaptchaBonus'),
    re_path(r'^fe/wishlist/page/checkbox/captcha/bonus/$', views.front_WishlistCheckBoxCaptcha, name='frontWishlistCheckBoxCaptchaBonus'),
    re_path(r'^fe/purchase/credit/page/checkbox/captcha/bonus/$', views.front_PurchaseCreditCheckBoxCaptcha, name='frontPurchaseCreditCheckBoxCaptchaBonus'),
    re_path(r'^fe/purchase/credit/payment/page/checkbox/captcha/bonus/$', views.front_CreditPurchasePaymntCheckBoxCaptcha, name='frontPurchaseCreditPaymentPgCheckBoxCaptchaBonus'),

    re_path(r'^fe/purchase/credit/payment/success/page/checkbox/captcha/bonus/$', views.front_CreditPurchaseSuccessCheckBoxCaptcha, name='frontPurchaseCreditPaymentSccessPgCheckBoxCaptchaBonus'),
    re_path(r'^fe/winning/chance/purchase/success/page/checkbox/captcha/bonus/$', views.front_WnChancePurchaseSccMsgCheckBoxCaptcha, name='frontWinningChancePymntSccessPgCheckBoxCaptchaBonus'),


    # invisible captcha solving
    re_path(r'^fe/invisible/captcha/bonus/$', views.front_invisibleCaptchaBonus, name='frontInvisibleCaptchaBonus'),

    re_path(r'^fe/login/register/$', views.front_loginRegister, name='frontEndLoginRegister'),
    re_path(r'^fe/login/user/$', views.front_loginUser, name="frontEndLoginUser"),

    # forgot password
    re_path(r'^fe/provide/email/to/reset/password/$', views.front_give_email_to_reset_pass, name='frontGiveEmailResetPassword'),
    re_path(r'^fe/reset/password/(?P<username>\w+)/$', views.front_reset_password, name='frontResetPassword'),

    # search
    re_path(r'^fe/search/$', views.front_search, name='frontSearch'),

    # shop by category
    re_path(r'^fe/shop/(?P<pk>\d+)/$', views.front_shop, name='frontShop'),

    # shop for all category
    re_path(r'^fe/shop/for/all/category/$', views.front_shop_for_all_category, name='frontShopForAllCategory'),

    # product details
    re_path(r'^fe/product/details/(?P<product_id>[-\w]+)/$', views.front_productDetails, name='frontEndProductDetails'),

    # user profile section **************************
    re_path(r'^fe/buyer/user/profile/(?P<username>\w+)/$', views.front_user_profile, name='frontEndUserProfile'),

    re_path(r'^fe/add/default/billing/infor/$', views.front_add_default_billing_info, name='frontAddDefaultBillingInfo'),
    re_path(r'^fe/update/billing/infor/(?P<pk>\d+)/$', views.front_update_default_billing_info, name='frontUpdateDefaultBillingInfo'),
    re_path(r'^fe/del/billing/info/(?P<pk>\d+)/$', views.front_delete_default_billing_info, name='frontDeleteDefaultBillingInfo'),

    re_path(r'^fe/add/default/shipping/infor/$', views.front_add_default_shipping_info, name='frontAddDefaultShippingInfo'),
    re_path(r'^fe/update/shipping/infor/(?P<pk>\d+)/$', views.front_update_default_shipping_info, name='frontUpdateDefaultShippingInfo'),
    re_path(r'^fe/del/shipping/info/(?P<pk>\d+)/$', views.front_delete_default_shipping_info, name='frontDeleteDefaultShippingInfo'),

    # move prize product to prize cart
    re_path(r'^fe/add/to/prize/cart/(?P<product_id>[-\w]+)/(?P<username>[-\w]+)/$', views.front_move_prizes_toPrizeCart, name='frontMoveToPrizeCart'),
    re_path(r'^fe/prize/cart/items/(?P<username>[-\w]+)/$', views.front_prize_cart_items, name='frontPrizeCartItems'),
    re_path(r'^fe/prize/checkout/(?P<username>[-\w]+)/$', views.front_prize_checkout, name='frontPrizeCheckout'),
    re_path(r'^fe/confirm/prize/delivery/order/(?P<username>[-\w]+)/$', views.front_confirm_prize_delivery_order, name='frontConfirmPrizeDeliveryOrder'),

    # convert point into credit points
    re_path(r'^fe/convert/point/into/wallet/(?P<username>[-\w]+)/$', views.front_ConvertPointInto_credit, name='frontConvertPointIntoCredit'),

    # user invitation
    re_path(r'^fe/send/mail/invitation/$', views.front_send_email_invitation, name='frontSendEmailInvitation'),
    # referal link
    re_path(r'^fe/refer/get/bonus/$', views.front_refer_and_get_bonusPoint, name='frontReferGet500Bonus'),
    re_path(r'^fe/(?P<username>[-\w]+)/(?P<referal_code>[-\w]+)/$', views.front_track_and_give_bonus_to_referer, name='frontTrackReferer'),

    # re_path(r'^fe/logout/shopper/$', views.frontLogouShopper, name='frontEndLogoutUser'),
    re_path(r'^front/logg_out/user/$', views.frontLogoutShopper, name='frontLoggOutShopper'),
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

    # buy credit
    re_path(r'^fe/buy/credit/points/(?P<username>[-\w]+)/$', views.front_buy_credit_point, name='frontBuyCreditPoint'),
    re_path(r'^fe/pay/for/purchasing/credit/point/$', views.front_pay_for_purchasing_point, name='frontPayForPurchasingPoint'),
    re_path(r'^fe/purchase/credit/success/msg/(?P<username>[-\w]+)/$', views.fron_credit_purchase_success_msg, name='frontCreditPurchaseSuccessMsg'),

    # leave review
    re_path(r'^fe/leave/review/(?P<product_id>[-\w]+)/$', views.front_leave_product_review, name="frontLeaveProductReview"),

    # wishlist
    re_path(r'^fe/add/to/wishlist/(?P<product_id>[-\w]+)/$', views.front_add_to_wishlist, name='frontAddToWishlist'),
    re_path(r'^fe/wishlist/(?P<username>[-\w]+)/$', views.front_wishlist, name='frontWishlist'),
    re_path(r'^fe/remove/item/wishlist/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.front_remove_item_from_wishlist, name='frontRemoveItemFromWishlist'),

    # gameing urls and winning chance purchase
    re_path(r'^fe/game/$', views.front_game, name='frontGame'),
    re_path(r'^fe/buy/winning/chance/$', views.front_buy_winning_chance, name='frontBuyWinningChance'),
    re_path(r'^fe/pay/for/game/purchasing/chance/$', views.front_pay_for_purchasing_wnning_chance, name='frontPayForPurchasingGame'),
    re_path(r'^fe/purchaing/winning/chance/success/message/(?P<username>[-\w]+)/$', views.front_winning_chance_purchasing_succss_msg, name="frontWinningChancePurchasingSccssMsg"),
    # payment successfull message purchasing product
    re_path(r'^fe/payment/successfull/msg/(?P<username>[-\w]+)/$', views.front_payment_successfull_msg, name='frontPaymentSuccessfullmsg'),

    # game terms policies
    re_path(r'^fe/game/terms/policies/$', views.front_game_terms_policies, name='frontGameTermsPolicies'),

    # policy section
    re_path(r'^fe/beta/test/terms/condition/$', views.front_BetatestTerms_andCondition, name='frontBetaTestTermsCondition'),
    re_path(r'^fe/refund/policy/$', views.front_refund_policy, name='frontRefundPolicy'),
    re_path(r'^fe/return/policy/$', views.front_return_policy, name='frontReturnPolicy'),
    re_path(r'^fe/security/policy/$', views.front_security_policy, name='frontSecurityPolicy'),
    re_path(r'^fe/delivery/policy/$', views.front_delivery_policy, name='frontDeliveryPolicy'),

    re_path(r'^fe/members/policy/details/$', views.front_MembershipPolicy, name='frontMembersPolicy'),
    re_path(r'^fe/shopper/policy/details/$', views.front_ShopperPolicy, name='frontShopperPolicy'),

    # company
    re_path(r'^fe/about/us/$', views.front_about_us, name='frontAboutUs'),
    re_path(r'^fe/cookie/policy/$', views.front_cookie_policy, name='frontCookiePolicy'),
    re_path(r'^fe/terms/condition/$', views.front_terms_conditions, name='frontTermsCondition'),
    re_path(r'^fe/privacy/policy/$', views.front_privacy_policy, name='frontPrivacyPolicy'),

    # sign up for newletter
    re_path(r'^fe/sign_up/newletter/$', views.front_signup_for_newletter, name='fronSignupForNewletter'),
    re_path(r'^fe/contact/us/$', views.front_contact_us, name='frontContactUs'),

    # how it works***********************************************************************
    # re_path(r'^fe/how/spinwin/works/$', views.front_how_spinWinWorks, name='frontHowSpinWinWorks'),
    re_path(r'^fe/how/it/works/account/details/$', views.front_howIt_account_details, name='frontfront_howIt_account_details'),
    re_path(r'^fe/how/spinit2win/works/$', views.front_howIt_howSpinit2Win_works, name='front__howSpinit2WinWorks'),
    re_path(r'^fe/how/works/spin/tokens/$', views.front_howIt__spin_tokens, name='front__howWorks_spintokens'),
    re_path(r'^fe/how/works/spin/credits/$', views.front_howIt__spinCredit, name='front__howWorks_spinCredits'),
    re_path(r'^fe/how/works/prize/guide/$', views.front_howIt__prizeGuide, name='front__howWorks_prizeGuide'),
    re_path(r'^fe/how/works/spin/pilot/promo/$', views.front_howIt__spinPilotPromotion, name='front__howWorks_spinPromotion'),
    re_path(r'^fe/how/woks/account/details/$', views.front_howIt__accountDetails, name='front__howWorks_AccountDetails'),
]
