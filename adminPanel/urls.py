from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [

    # re_path(r'^ap/create/order/$', views.create_order, name='createOrder'),

    re_path(r'^ap/authorization/$', views.authorizationAPI, name='authoRizationAPi'),
    re_path(r'^ap/check/api/$', views.checkAPI, name='checkAPI'),

    # login-register
    re_path(r'^ap/register/updated/$', views.ap_RegisterSuperUser, name="apSuperAdminRegister"),
    re_path(r'^ap/login/updated/$', views.ap_loginSuperUser, name="apSuperAdminLogin"),
    re_path(r'^ap/logout/super/user/$', views.logoutSuperUser, name="apLogoutSuperUser"),

    re_path(r'^index/$', views.index, name="apIndex"),
    re_path(r'^ap/home/$', views.home, name="apHome"),

    # spin point given user list
    re_path(r'^ap/total/spin/point/given/user/list/$', views.ap_sping_point_givenUserList, name='ap_sping_point_givenUserList'),

    # spin point given user list
    re_path(r'^ap/total/spin/credit/given/user/list/$', views.ap_sping_credit_givenUserList, name='ap_sping_credit_givenUserList'),

    # spin tokens given user list
    re_path(r'^ap/total/spin/tokens/given/user/lists/$', views.ap_sping_tokens_givenUserList, name='ap_sping_tokens_givenUserList'),

    # spin credit purhase history
    re_path(r'^ap/spin/credit/purchase/history/$', views.ap_spin_credit_purchase_history, name='apSpinCreditPurchaseHistory'),

    # spin token purhase history
    re_path(r'^ap/spin/token/purchase/history/$', views.ap_spin_token_purchase_history, name='apSpinTokenPurchaseHistory'),

    # product purchase history
    re_path(r'^ap/product/purchase/history/$', views.ap_product_purchaseHistory, name='apProductPurchaseHistory'),

    re_path(r'^ap/deactivate/user/(?P<pk>\d+)/$', views.deactivateUser, name="apDeactivateuser"),
    re_path(r'^ap/activate/user/(?P<pk>\d+)/$', views.activateUser, name="apActivateUser"),
    re_path(r'^ap/remove/user/(?P<pk>\d+)/$', views.removeUser, name="apRemoveUser"),


    # product category
    re_path(r'^ap/add/product/category/$', views.ap_add_product_category, name='apAddProductCategory'),
    re_path(r'^ap/edit/product/category/(?P<pk>\d+)/$', views.ap_edit_product_category, name='apEditProductCategory'),
    re_path(r'^ap/del/product/category/(?P<pk>\d+)/$', views.ap_del_product_category, name='apDelProductCategory'),

    # product subcategory
    re_path(r'^ap/add/subcategory/(?P<pk>\d+)/$', views.ap_add_product_subcat, name='apAddSubcategory'),
    re_path(r'^ap/del/subcategory/(?P<pk>\d+)/$', views.ap_del_product_subcat, name='apDelProductSubcateogory'),

    # woocommerce store section
    re_path(r'^ap/fetch/woocommerce/product/$', views.ap_fetch_woocommerce_store_prdct, name='apWoocommerceProduct'),
    re_path(r'^ap/update/woocommerce/product/$', views.ap_update_wocommerce_store_prdct, name='apUpdateWoocommerceProduct'),
    re_path(r'^ap/del/woocmrce/product/(?P<pk>\d+)/$', views.ap_del_woocmmrce_prdct, name='apDelWoocmrceProduct'),
    re_path(r'^ap/woocommerce/store/product/list/$', views.ap_woocommerce_store_list, name='apWoocommerceStoreList'),
    re_path(r'^ap/woocommerce/product/details/(?P<pk>\d+)/$', views.ap_wcmrce_prdct_details, name='apWoocmrcePrdctDetails'),

    # package part starts***********************************************************************************************
    re_path(r'^ap/add/new/package/name/$', views.ap_add_new_packageName, name='apAddNewPackageName'),
    re_path(r'^ap/update/package/name/(?P<pk>\d+)/$', views.ap_update_new_packageName, name='apUpdatePackageName'),
    re_path(r'^ap/remove/package/name/(?P<pk>\d+)/$', views.ap_remove_packageName, name='apRemovePackageName'),

    # package feature options
    re_path(r'^ap/add/package/feature/options/$', views.ap_add_packageFeatureOptions, name='apAddPackageFeatureOptions'),
    re_path(r'^ap/update/package/option/(?P<pk>\d+)/$', views.ap_update_packageFeatureOptions, name='apUpdatePackageFeatureOption'),
    re_path(r'^ap/remove/package/option/(?P<pk>\d+)/$', views.ap_remove_packageFeatureOption, name='apRemovePackageFeatureOption'),

    # packages
    re_path(r'^ap/add/package/$', views.ap_add_package, name='apAddPackage'),
    re_path(r'^ap/activate/package/(?P<pk>\d+)/$', views.ap_activate_package, name='apActivatePackage'),
    re_path(r'^ap/de_activate/package/(?P<pk>\d+)/$', views.ap_de_activate_package, name='apDe_ActivatePackage'),
    re_path(r'^ap/update/package/(?P<pk>\d+)/$', views.ap_update_package, name='apUpdatePackage'),
    re_path(r'^ap/delete/package/(?P<pk>\d+)/$', views.ap_remove_package, name='apRemovePackage'),


    # order section*********************************************

    re_path(r'^ap/current/order/list/$', views.ap_current_orders, name='apCurrentOrderList'),
    re_path(r'^ap/current/order/details/(?P<order_id>[-\w]+)/$', views.ap_current_order_details, name='apCurrentOrderDetails'),
    re_path(r'^ap/change/order/status/to/onTheWay/(?P<order_id>[-\w]+)/$', views.ap_set_crrnt_order_to_on_the_way, name='apSetCrrntOrderStatusToOnTheWay'),
    re_path(r'^ap/cancel/order/(?P<order_id>[-\w]+)/$', views.ap_cancel_order, name='apCancelOrder'),

    # on the way
    re_path(r'^ap/on/the/way/order/list/$', views.ap_on_the_way_order_list, name='apOnTheWayOrderList'),
    re_path(r'^ap/set/to/order/delivered/(?P<order_id>[-\w]+)/$', views.ap_set_to_delivered, name='apSetToOrderDelivered'),

    # deivered orders
    re_path(r'^ap/delivered/order/list/$', views.ap_delivered_order_list, name='apDeliveredOrderList'),

    # cancelled orders
    re_path(r'^ap/cacelled/order/list/$', views.ap_cancelled_order_list, name='apCanCelledOrderList'),

    # coupon section
    re_path(r'^ap/add/coupon/code/$', views.ap_add_couponCode, name='apAddCouponoCode'),
    re_path(r'^ap/coupon/code/list/$', views.ap_couponCode_list, name='apCouponCodeList'),
    re_path(r'^ap/coupon/code/activate/deactivate/(?P<pk>\d+)/$', views.ap_activate_orDeactivate_couponCode, name='apActivateOrDeactivateCouponCode'),
    re_path(r'^ap/update/coupon/code/(?P<pk>\d+)/$', views.ap_update_couponCode, name='apUpdateCouponCode'),
    re_path(r'^ap/del/coupon/code/(?P<pk>\d+)/$', views.ap_remove_couponCode, name='apDelCouponCode'),


    # updated product section ****************************************
    re_path(r'^ap/all/product/list/', views.ap_all_products, name='apAllProductList'),
    re_path(r'^ap/add/admin/custom/product/$', views.ap_add_admin_custsom_product, name='apAddAdminCustomProduct'),
    re_path(r'^ap/admin/custom/product/list/$', views.ap_admin_custom_product_list, name='apAdminCustomProductList'),
    re_path(r'^ap/admin/custom/product/details/(?P<pk>\d+)/(?P<product_id>[-\w]+)/$', views.ap_admin_custom_product_details, name='apAdminCustomProductDetails'),
    re_path(r'^ap/update/admin/custom/product/(?P<pk>\d+)/(?P<product_id>[-\w]+)/$', views.ap_update_admin_custom_product, name='apUpdateAdminCustomProduct'),
    re_path(r'^ap/del/admin/custom/product/(?P<pk>\d+)/$', views.ap_del_admin_custom_product, name='apDelAdminCustomProduct'),
    re_path(r'^ap/update/admin/woocmmerce/product/(?P<pk>\d+)/(?P<product_id>[-\w]+)/$', views.ap__update_admin_wcmrce_product, name='apUpdateAdminWocmrceProduct'),


    # game section starts ******************************************************
    re_path(r'^ap/game/settings/$', views.ap_game_settings, name='apGameSettings'),
    re_path(r'^ap/activate/game/segment/(?P<pk>\d+)/$', views.ap_activate_game_setting, name='apActivateGameSegment'),
    re_path(r'^ap/deactivate/game/segment/(?P<pk>\d+)/$', views.ap_deactivate_game_setting, name='apDeActivateGameSegment'),
    re_path(r'^ap/update/game/segment/(?P<pk>\d+)/$', views.ap_update_game_setting, name='apUpdateGameSegment'),
    re_path(r'^ap/del/game/segment/(?P<pk>\d+)/$', views.ap_delete_game_setting, name='apDeleteGameSegment'),
    re_path(r'^ap/applicable/rules/for/winning/prize/$', views.ap_applicable_rules_for_prize_winner, name='apApplicableRuleWinningPrize'),
    re_path(r'^ap/remove/product/with/applicable/rule/(?P<pk>\d+)/$', views.ap_remove_prduct_with_applicable_rules, name='apRemoveProductWithApplicableRule'),

    re_path(r'^ap/add/new/segment/$', views.ap_add_new_segment, name='apAddNewSegment'),
    re_path(r'^ap/remove/new/segment/(?P<pk>\d+)/$', views.ap_remove_new_segment, name='apRemoveSegment'),
    re_path(r'^ap/add/game/terms/policies/$', views.ap_add_terms_policies_forGame, name='apAddTermsPoliciesForGame'),
    re_path(r'^ap/update/game/terms/policies/(?P<pk>\d+)/$', views.ap_update_terms_policies_forGame, name='apUpdateGameTermsPolicies'),
    re_path(r'^ap/del/game/terms/policies/(?P<pk>\d+)/$', views.ap_delete_terms_policies_forGame, name='apDeleteGameTermsPoliciesForGame'),

    # gaming sponsored product list
    re_path(r'^ap/game/sponsored/products/$',views.ap_sponsored_prdacts_for_game, name='apGameSponsoredProducts'),
    re_path(r'^ap/del/game/sponsored/product/(?P<pk>\d+)/$', views.ap_del_sponsored_product, name='apDelSpnsoredProduct'),

    re_path(r'^ap/game/activate/sponsored/product/for/win/(?P<pk>\d+)/$', views.ap_activate_spnsored_prdct_for_game, name='apActivateSponsoredProductForGame'),
    re_path(r'^ap/game/de_activate/sponsored/product/for/win/(?P<pk>\d+)/$', views.ap_deactivate_sponsord_prdct_for_game, name='apDeActivateSponsoredProductForGame'),

    re_path(r'^ap/segment/setting/$', views.ap_segment_setting, name='apSegmentSettings'),
    re_path(r'^ap/activate/segment/(?P<pk>\d+)/$', views.ap_activate__segment, name='apActivateSegment'),
    re_path(r'^ap/de_activate/segment/(?P<pk>\d+)/$', views.ap_deactivate__segment, name='apDe_ActivateSegment'),
    re_path(r'^ap/update/segemnt/setting/(?P<pk>\d+)/$', views.ap_update_segment_setting, name='apUpdateSegmentSetting'),
    re_path(r'^ap/del/segemnt/setting/(?P<pk>\d+)/$', views.ap_del_segment_setting, name='apDeleteSegmentSetting'),


    # acccounts list section ***********************************
    re_path(r'^ap/seller/accounts/list/$', views.ap_seller_accounts_list, name='apsellerAccountsList'),
    re_path(r'^ap/buyer/acccounts/list/$', views.ap_buyer_accounts_list, name='apBuyerAccountsList'),
    re_path(r'^ap/remove/buyer/account/(?P<pk>\d+)/$', views.ap_remove_buyer_account, name='apRemoveBuyerAccount'),

    re_path(r'^ap/buyer/details/(?P<pk>\d+)/$', views.ap_single_buyer_details, name='apSingleBuyerDetails'),

    # add spin point to shopper account from admin panel
    re_path(r'^ap/add/spin/point/to/shopper/account/(?P<pk>\d+)/$', views.ap_add_spinPointToShopperAccntFromAP, name='apAddSpinPointToShopperAccntFromAP'),
    re_path(r'^ap/add/spin/credit/to/shopper/account/(?P<pk>\d+)/$', views.ap_add_spinCreditToShopperAccntFromAP, name='apAddSpinCreditToShopperAccntFromAP'),
    re_path(r'^ap/add/spin/tokens/to/shopper/account/(?P<pk>\d+)/$', views.ap_add_spinTokensToShopperAccntFromAP, name='apAddSpinTokensToShopperAccntFromAP'),

    # change buyer fname
    re_path(r'^ap/change/buyer/fname/(?P<pk>\d+)/$', views.ap_change_buyer_fname, name='apChangeBuyerFname'),

    # change buyer lname
    re_path(r'^ap/change/buyer/lname/(?P<pk>\d+)/$', views.ap_change_buyer_lname, name='apChangeBuyerLname'),

    # change buyer email
    re_path(r'^ap/change/buyer/email/(?P<pk>\d+)/$', views.ap_change_buyer_email, name='apChangeBuyerEmail'),

    # change buyer username
    re_path(r'^ap/change/buyer/username/(?P<pk>\d+)/$', views.ap_change_buyer_username, name='apChangeBuyerUsername'),

    # change buyer username
    re_path(r'^ap/change/buyer/phone/no/(?P<pk>\d+)/$', views.ap_change_buyer_phoneNo, name='apChangeBuyerPhoneNo'),

    # change buyer account activation status
    re_path(r'^ap/change/buyer/account/activation/status/(?P<pk>\d+)/$', views.ap_change_buyer_account_activation_status, name='apChangeBuyerAcntActivationStatus'),

    # change buyer account change buyer password
    re_path(r'^ap/change/buyer/account/change/password/(?P<pk>\d+)/$', views.ap_change_buyer_account_reset_password, name='apChangeBuyerChangeBuyerPassword'),

    # single user captcha history
    re_path(r'^ap/shopper/captcha/history/(?P<pk>\d+)/$', views.ap_singleShopperCaptcha_history, name='apSingleShopperCaptchaHistory'),

    # daily sign in bonus history
    re_path(r'^ap/shopper/daily/sign/in/bonus/history/(?P<pk>\d+)/$', views.ap_singleShopperDailySignInBonusPoint_history, name='ap_singleShopperDailySignInBonusPoint_history'),
    re_path(r'^ap/remove/shopper/daily/sign/in/bonus/history/(?P<user_pk>\d+)/(?P<obj_pk>\d+)/$', views.ap_singleRemoveShopperDailySignInBonusPoint_history, name='ap_singleRemoveShopperDailySignInBonusPoint_history'),

    # email invitation bonus history
    re_path(r'^ap/shopper/email/invitation/bonus/history/(?P<pk>\d+)/$', views.ap_singleShopperEmailInvitationBonsHistory, name='ap_singleShopperEmailInvitationBonsHistory'),
    re_path(r'^ap/remove/shopper/email/invitation/bonus/history/(?P<user_pk>\d+)/(?P<obj_pk>\d+)/$', views.ap_RemoveSingleShopperEmailInvitationBonsHistory, name='ap_RemoveSingleShopperEmailInvitationBonsHistory'),

    # referal bonus history
    re_path(r'^ap/shopper/referla/bonus/history/(?P<pk>\d+)/$', views.ap_singleShopperReferalBonsHistory, name='ap_singleShopperReferalBonsHistory'),
    re_path(r'^ap/remove/shopper/referal/bonus/history/(?P<user_pk>\d+)/(?P<obj_pk>\d+)/$', views.ap_RemoveSingleShopperReferalBonsHistory, name='ap_RemoveSingleShopperReferalBonsHistory'),

    # single user spin credit purchase history
    re_path(r'^ap/single/shopper/spin/credit/purchase/history/(?P<user_pk>\d+)/$', views.ap_single_shopper_credit_point_purchaseHistory, name='ap_single_shopper_credit_point_purchaseHistory'),

    # single user spin token purchase history
    re_path(r'^ap/single/shopper/spin/token/purchase/history/(?P<user_pk>\d+)/$', views.ap_singleShopper_spinTokenPrchaseHistory, name='ap_singleShopper_spinTokenPrchaseHistory'),

    # single user spin token spending history history
    re_path(r'^ap/single/shopper/spin/token/spending/history/(?P<user_pk>\d+)/$', views.ap_singleShopper_spinTokenSpendingHistory, name='ap_singleShopper_spinTokenSpendingHistory'),



    re_path(r'^ap/staff/accounts/list/$', views.ap_staff_accounts_list, name= 'apStaffAccountsList'),

    # site_setting section *******************************************************

    # top footer section
    re_path(r'^ap/top/footer/setting/$', views.ap_top_footer_setting, name='apTopFooterSetting'),
    re_path(r'^ap/free/delivery/setting/$', views.ap_free_delivery_setting, name='apFreeDeliverySetting'),
    re_path(r'^ap/del/free/delivery/setting/(?P<pk>\d+)/$', views.ap_del_free_delivery_setting, name='apDelFreeDeliverySetting'),

    re_path(r'^ap/safe/payment/setting/$', views.ap_add_safe_payment_setting, name='apAddSafePaymentSetting'),
    re_path(r'^ap/del/safe/payment/setting/(?P<pk>\d+)/$', views.ap_del_safe_payment_setting, name='apDelSafePaymentSetting'),

    re_path(r'^ap/shop/with/confidence/setting/$', views.ap_shop_with_confident_setting, name='apAddShopWithConfidence'),
    re_path(r'^ap/del/shop/with/confidence/setting/(?P<pk>\d+)/$', views.ap_del_shop_with_confident_setting, name='apDelShopWithConfidence'),

    re_path(r'^ap/24_7/help/center/setting/$', views.ap_add_help_center_setting, name='apAddHelpCenterSetting'),
    re_path(r'^ap/del/24_7/help/center/setting/(?P<pk>\d+)/$', views.ap_del_help_center_setting, name='apDelHelpCenterSetting'),

    re_path(r'^ap/about/us/$', views.ap_about_us, name='apAboutUs'),
    re_path(r'^ap/del/about/us/(?P<pk>\d+)/$', views.ap_del_about_us, name='apDelAboutUs'),
    re_path(r'ap/edit/about/us/(?P<pk>\d+)/$', views.ap_edit_about_us, name='apEditAboutUs'),

    re_path(r'^ap/contact/us/$', views.ap_contact_us, name='apcontactUs'),
    re_path(r'^ap/edit/contact/us/(?P<pk>\d+)/$', views.ap_edit_contact_us, name='apEditContactUs'),
    re_path(r'^ap/del/contact/us/(?P<pk>\d+)/$', views.ap_del_contact_us, name='apDelContactUs'),

    # policy setting ***************************************************

    # beta test terms conditions
    re_path(r'^ap/add/beta/test/terms/condition/$', views.ap_add_betaTest_termsConditions, name='apAddBetaTestTermsConditions'),
    re_path(r'^ap/update/beta/test/terms/conditions/(?P<pk>\d+)/$', views.ap_update_betaTest_termsConditions, name='apUpdateBetaTestTermsConditions'),
    re_path(r'^ap/remove/beta/test/terms/conditions/(?P<pk>\d+)/$', views.ap_removeBetaTestTermsCondition, name='apRemoveBetaTestTermsConditions'),

    # members policy
    re_path(r'^ap/add/members/policy/$', views.ap_add_MembersPolicy, name='apAddMembersPolicy'),
    re_path(r'^ap/update/members/policy/(?P<pk>\d+)/$', views.ap_update_MembersPolicy, name='apUpdateMembersPolicy'),
    re_path(r'^ap/remove/members/policy/(?P<pk>\d+)/$', views.ap_removeMembersPolicy, name='apRemoveMembersPolicy'),

    # shopper policy
    re_path(r'^ap/add/shopper/policy/$', views.ap_add_ShopperPolicy, name='apAddShopperPolicy'),
    re_path(r'^ap/update/shopper/policy/(?P<pk>\d+)/$', views.ap_update_ShopperPolicy, name='apUpdateShopperPolicy'),
    re_path(r'^ap/remove/shopper/policy/(?P<pk>\d+)/$', views.ap_removeShopperPolicy, name='apRemoveShopperPolicy'),

    re_path(r'^ap/delivery/policy/$', views.ap_delivery_policy, name='apDeliveryPolicy'),
    re_path(r'^ap/update/delivery/policy/(?P<pk>\d+)/$', views.ap_update_delivery_policy, name='apUpdateDeliveryPolicy'),
    re_path(r'^ap/del/delivery/policy/(?P<pk>\d+)/$', views.ap_del_delivery_policy, name='apDeleteDeliveryPolicy'),

    # product return policy
    re_path(r'^ap/add/return/policy/$', views.ap_add_return_policy, name='apAddReturnPolicy'),
    re_path(r'^ap/update/return/policy/(?P<pk>\d+)/$', views.ap_update_return_policy, name='apUpdateReturnPolicy'),
    re_path(r'^ap/delete/return/policy/(?P<pk>\d+)/$', views.ap_del_return_policy, name='apDeleteReturnPolicy'),

    # product refund policy
    re_path(r'^ap/add/refund/policy/$', views.ap_add_refund_policy, name='apAddRefundPolicy'),
    re_path(r'^ap/update/refund/policy/(?P<pk>\d+)/$', views.ap_update_refund_policy, name='apUpdateRefundPolicy'),
    re_path(r'^ap/delete/refund/policy/(?P<pk>\d+)/$', views.ap_del_refund_policy, name='apDeleteRefundPolicy'),

    # product refund policy
    re_path(r'^ap/add/security/policy/$', views.ap_add_security_policy, name='apAddSecurityPolicy'),
    re_path(r'^ap/update/security/policy/(?P<pk>\d+)/$', views.ap_update_security_policy, name='apUpdateSecurityPolicy'),
    re_path(r'^ap/delete/seccurity/policy/(?P<pk>\d+)/$', views.ap_del_security_policy, name='apDeleteSecurityPolicy'),

    # product terms & conditions
    re_path(r'^ap/add/terms/condition/policy/$', views.ap_add_termCondition_policy, name='apAddTermsConditionPolicy'),
    re_path(r'^ap/update/terms/condition/policy/(?P<pk>\d+)/$', views.ap_update_termCondition_policy, name='apUpdateTermsConditionPolicy'),
    re_path(r'^ap/delete/term/condition/policy/(?P<pk>\d+)/$', views.ap_del_termCondition_policy, name='apDeleteTermsConditionPolicy'),

    # product privacy policy
    re_path(r'^ap/add/product/privacy/policy/$', views.ap_add_ProductPrivacy_policy, name='apAddProductPrivacyPolicy'),
    re_path(r'^ap/update/product/privacy/policy/(?P<pk>\d+)/$', views.ap_update_ProductPrivacy_policy, name='apUpdateProductPrivacyPolicy'),
    re_path(r'^ap/delete/product/privacy/policy/(?P<pk>\d+)/$', views.ap_del_ProductPrivacy_policy, name='apDeleteProductPrivacyPolicy'),

    # product privacy policy
    re_path(r'^ap/add/cookie/policy/$', views.ap_add_cookie_policy, name='apAddCookiePolicy'),
    re_path(r'^ap/update/cookie/policy/(?P<pk>\d+)/$', views.ap_update_cookie_policy, name='apUpdateCookiePolicy'),
    re_path(r'^ap/delete/cookie/policy/(?P<pk>\d+)/$', views.ap_del_cookie_policy, name='apDeleteCookiePolicy'),

    # profile section ***************************************************
    re_path(r'^ap/my/profile/(?P<username>\w+)/$', views.ap_my_profile, name='apMyProfile'),
    re_path(r'^ap/update/profile/picture/$', views.ap_update_user_profile_picture, name='apUpdateUserProfilePicture'),
    re_path(r'^ap/update/user/full/name/$', views.ap_update_user_full_name, name='apUpdateUserProfileFullname'),
    re_path(r'^ap/update/user/password/$', views.ap_update_user_password, name='apUpdateUserPassword'),

    # Home page main banner section starts ****************************************************
    re_path(r'^ap/add/banner/$', views.ap_add_banner, name='apAddBanner'),
    re_path(r'^ap/banner/list/$', views.ap_banner_list, name='apBannerList'),
    re_path(r'^ap/update/banner/(?P<pk>\d+)/(?P<banner_id>[-\w]+)/$', views.ap_update_banner, name='apUpdateBannerInfo'),
    re_path(r'^ap/banner/(?P<pk>\d+)/(?P<banner_id>[-\w]+)/details/$', views.ap_banner_details, name='apBannerDetails'),
    re_path(r'^ap/del/banner/(?P<pk>\d+)/$', views.ap_del_banner, name='apDelBanner'),

    # home page mini top banner
    re_path(r'^ap/add/home/page/mini/top/banner/$', views.ap_home_pageMini_topBanner, name='apAddHomePageMiniTopBanner'),
    re_path(r'^ap/home/page/mini/top/banner/list/$', views.ap_home_pageMini_topBanrList, name='apHomePageMiniTopBannerList'),
    re_path(r'^ap/home/page/activate/top/mini/banner/(?P<pk>\d+)/$', views.ap_activate_home_pageMini_topBanr, name='apHomeActivateTopBanner'),
    re_path(r'^ap/home/page/de_activate/top/mini/banner/(?P<pk>\d+)/$', views.ap_de_activate_home_pageMini_topBanr, name='apHomeDe_ActivateTopBanner'),
    re_path(r'^ap/home/page/deleted/top/mini/banner/(?P<pk>\d+)/$', views.ap_delete_home_pageMiniTopBanner, name='apHomeDeleteTopBanner'),

    # home page mini top banner
    re_path(r'^ap/add/home/page/mini/bottom/banner/$', views.ap_home_pageMini_bottomBanner, name='apAddHomePageMiniBottomBanner'),
    re_path(r'^ap/home/page/mini/bottom/banner/list/$', views.ap_home_pageMini_BottomBanrList, name='apHomePageMiniBottomBannerList'),
    re_path(r'^ap/home/page/activate/mini/bottom/banner/(?P<pk>\d+)/$', views.ap_activate_home_pageMini_BottomBanr, name='apActivateHomePageMiniBottomBanner'),
    re_path(r'^ap/home/page/de_activate/mini/bottom/banner/(?P<pk>\d+)/$', views.ap_de_activate_home_pageMini_bottomBanr, name='apDe_ActivateHomePageMiniBottomBanner'),
    re_path(r'^ap/home/page/delete/mini/bottom/banner/(?P<pk>\d+)/$', views.ap_delete_home_pageMiniBottomBanner, name='apDeleteHomePageMiniBottomBanner'),


    # user profile page ads section
    re_path(r'^ap/add/ads/user/profile/pg/$', views.ap_add_ads_toUser_profilePage, name='apAddAdsToUserProfilePg'),
    re_path(r'^ap/user/profile/ads/list/$', views.ap_user_profile_ads_list, name='apUserProfileAdsList'),
    re_path(r'^ap/del/user/profile/ads/(?P<pk>\d+)/$', views.ap_del_usr_profile_ads, name='apDelUserProfileAds'),
    re_path(r'^ap/activate/user/profile/ads/(?P<pk>\d+)/$', views.ap_activate_usr_profile_ads, name='apActivateUserProfileAds'),
    re_path(r'^ap/de_activate/user/profile/ads/(?P<pk>\d+)/$', views.ap_deactivate_usr_profile_ads, name='apDe_ActivateUserProfileAds'),


    # logo section **********************************************
    re_path(r'^ap/add/logo/$', views.ap_add_site_logo, name='apAddSiteLogo'),
    re_path(r'^ap/del/site/logo/(?P<pk>\d+)/$', views.ap_del_site_logo, name='apDelSiteLogo'),

    # advertisement section
    re_path(r'^ap/add/banner/product/details/page/$', views.ap_add_banner_at_prod_detail_page, name='apAddBnrProdDetialPg'),
    re_path(r'^ap/product/details/pg/banner/list/$', views.ap_prod_details_pg_banner_list, name='apProductDetailsPgBnrList'),
    re_path(r'^ap/del/prod/detail/pg/banner/(?P<pk>\d+)/$', views.ap_del_prod_details_pg_banner, name='apDelProdDetialsPgBnr'),
    re_path(r'^ap/activate/prod/detail/pg/banner/(?P<pk>\d+)/$', views.ap_activate_prod_details_pg_banner, name='apActivateProdDetialsPgBnr'),
    re_path(r'^ap/de_activate/prod/detail/pg/banner/(?P<pk>\d+)/$', views.ap_de_activate_prod_details_pg_banner, name='apDe_ActivateProdDetialsPgBnr'),

    # banner on shop page
    re_path(r'^ap/add/shop/page/banner/$', views.ap_add_shop_page_banner, name='apAddShopPageBanner'),
    re_path(r'^ap/shop/page/banner/list/$', views.ap_shop_page_banner_list, name='apShopPageBannerList'),
    re_path(r'^ap/del/shop/page/banner/(?P<pk>\d+)/$', views.ap_delete_shop_page_banner, name='apDelShopPageBanner'),

    re_path(r'^ap/de_activate/shop/page/banner/(?P<pk>\d+)/$', views.ap_de_activate_shop_page_banner, name='apDe_ActivateShopPageBanner'),
    re_path(r'^ap/activate/shop/page/banner/(?P<pk>\d+)/$', views.ap_activate_shop_page_bannr, name='apActivateShopPageBanner'),

    # newsletter/subscriber list
    re_path(r'^ap/subscriber/list/$', views.ap_subscriber_list, name='apSubscriberList'),
    re_path(r'^ap/remove/subscriber/(?P<pk>\d+)/$', views.ap_remove_subscriber, name='apRemoveSubscriber'),

    # customer message list
    re_path(r'^ap/customer/message/list/$', views.ap_customer_msg_list, name='apCustomerMessageList'),
    re_path(r'^ap/del/customer/message/list/(?P<pk>\d+)/$', views.ap_del_customer_msg, name='apDelCustomerMessageList'),

    # analytics part starts******************************************************************************************

    re_path(r'^ap/analytics/home/$', views.ap_analytics_home, name='apAnalyticsHome'),

    # vistiots'info
    re_path(r'^ap/unique/visitors/list/$', views.ap_unique_visitors_list, name='apUniqueVisitorsList'),
    re_path(r'^ap/remove/unique/visitors/(?P<pk>\d+)/$', views.ap_remove_visitor_from_uniqueVisitorList, name='apUniqueVisitorsInfo'),

    # registered user
    re_path(r'^ap/registered/user/list', views.ap_registered_userList, name='apRegisteredUserList'),
    re_path(r'^ap/remove/user/userlist/(?P<pk>\d+)/$', views.ap_remove_userFromUserList, name='apRemmoveUserFromUsrList'),

    # point history
    re_path(r'^ap/user/given/bonus/point/history/$', views.ap_givenPointBonusHistory, name='apGivenPoinBonusHistory'),
    re_path(r'^ap/daily/signIn/bonus/user/list/$', views.ap_dailySignInBonusUserList, name='apDailySignInBonusUserList'),
    re_path(r'^ap/remove/daily/signIn/bonus/user/list/(?P<pk>\d+)/$', views.ap_removeDailySignInBonusUserList, name='apRemoveDailySignInBonusUserList'),

    # registered user bonus point list
    re_path(r'^ap/bonus/user/list/for/registering/$', views.ap_registrationBonusUserList, name='ap_registrationBonusUserList'),
    re_path(r'^ap/remove/bonus/user/list/for/registering/(?P<pk>\d+)/$', views.ap_remove_registrationBonusUserList, name='ap_remove_registrationBonusUserList'),

    # referal user bonus point list
    re_path(r'^ap/bonus/user/for/refering/$', views.ap_referalBonusUserList, name='ap_referalBonusUserList'),
    re_path(r'^ap/remove/bonus/user/for/refering/(?P<pk>\d+)/$', views.ap_remove_referalBonusUserList, name='ap_remove_referalBonusUserList'),

    # referal user bonus point list
    re_path(r'^ap/email/invitation/bonus/user/list/$', views.ap_emailInvitationBonusUserList, name='ap_emailInvitationBonusUserList'),
    re_path(r'^ap/remove/email/invitation/bonus/user/list/(?P<pk>\d+)/$', views.ap_remove_emailInvitationBonusUserList, name='ap_remove_emailInvitationBonusUserList'),



    # captcha history
    re_path(r'^ap/all/page/captcha/bonus/list/$', views.ap_all_pg_captcha_bonus_list, name='apAllPageCaptchaBonusList'),

    re_path(r'^ap/home/page/captcha/bonus/list/$', views.ap_home_pg_captcha_bonus_list, name='apHomePageCaptchaBonusList'),
    re_path(r'^ap/remove/home/page/captcha/(?P<pk>\d+)/bonus/$', views.ap_remove_homePg_captcha_bonus, name='apRemoveHomePageCaptchaBonusList'),

    # shop page
    re_path(r'^ap/shop/page/captcha/bonus/list/$', views.ap_shop_pg_captcha_bonus_list, name='apShopPageCaptchaBonusList'),
    re_path(r'^ap/remove/shop/page/captcha/(?P<pk>\d+)/bonus/$', views.ap_remove_shopPg_captcha_bonus, name='apRemoveShopPageCaptchaBonusList'),

    # shop page by category
    re_path(r'^ap/shop/page/by/category/captcha/bonus/list/$', views.ap_shop_pgByCat_captcha_bonus_list, name='apShopPageByCatCaptchaBonusList'),
    re_path(r'^ap/remove/shop/page/by/category/captcha/(?P<pk>\d+)/bonus/$', views.ap_remove_shopPgByCat_captcha_bonus, name='apRemoveShopPageByCatCaptchaBonusList'),

    # product details page by category
    re_path(r'^ap/product/details/page/captcha/bonus/list/$', views.ap_productDetails_pg_captcha_bonus_list, name='apProductDetailsPageByCatCaptchaBonusList'),
    re_path(r'^ap/remove/product/details/page/captcha/(?P<pk>\d+)/bonus/$', views.ap_remove_productDetails_captcha_bonus, name='apRemovePrdctDetailsPgCaptchaBonusList'),

    # game page
    re_path(r'^ap/game/page/captcha/bonus/list/$', views.ap_game_pg_captcha_bonus_list, name='apGamePageByCatCaptchaBonusList'),
    re_path(r'^ap/remove/game/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_gamePg_captcha_bonus, name='apRemoveGamePgCaptchaBonusList'),

    # user profile page
    re_path(r'^ap/user/profile/page/captcha/bonus/list/$', views.ap_userProfile_pg_captcha_bonus_list, name='apUserProfilePageCaptchaBonusList'),
    re_path(r'^ap/remove/user/profile/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_userProfilePg_captcha_bonus, name='apRemoveUsrProfilePgCaptchaBonusList'),

    # buy winning chance page
    re_path(r'^ap/buy/winning/chance/page/captcha/bonus/list/$', views.ap_buyWinningChance_pg_captcha_bonus_list, name='apBuyWinningChancePageCaptchaBonusList'),
    re_path(r'^ap/remove/buy/winning/chance/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_buyWinningChance_captcha_bonus, name='apRemoveBuyWinningChanceCaptchaBonusList'),

    # cart page
    re_path(r'^ap/cart/page/captcha/bonus/list/$', views.ap_cart_pg_captcha_bonus_list, name='apCartPgCaptchaBonusList'),
    re_path(r'^ap/remove/cart/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_cartPg_captcha_bonus, name='apRemoveCartCaptchaBonusList'),

    # contact us page
    re_path(r'^ap/contact/us/page/captcha/bonus/list/$', views.ap_contactUs_pg_captcha_bonus_list, name='apContactUsPgCaptchaBonusList'),
    re_path(r'^ap/remove/contact/us/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_contactUsPg_captcha_bonus, name='apRemoveContactUsCaptchaBonusList'),

    # winning chance payment page
    re_path(r'^ap/winning/chance/payment/page/captcha/bonus/list/$', views.ap_winning_chancePaymentPage_captcha_bonus_list, name='apWinningChancePaymentPgCaptchaBonusList'),
    re_path(r'^ap/remove/winning/chance/payment/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_winning_chancePaymentPage_captcha_bonus, name='apRemoveWinningChancePaymntPgCaptchaBonusList'),

    # product purchase payment page
    re_path(r'^ap/product/purchase/page/captcha/bonus/list/$', views.ap_productPurchasePage_captcha_bonus_list, name='apProductPurchasePgCaptchaBonusList'),
    re_path(r'^ap/remove/product/purchase/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_productPurchasePage_captcha_bonus, name='apRemoveProductPurchasePgCaptchaBonusList'),

    # product payment success page
    re_path(r'^ap/product/payment/success/page/captcha/bonus/list/$', views.ap_productPaymentSuccessPage_captcha_bonus_list, name='apProductPaymentSuccessPgCaptchaBonusList'),
    re_path(r'^ap/remove/product/payment/success/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_productPaymentSuccessPage_captcha_bonus, name='apRemoveProductPaymentSuccessPgCaptchaBonusList'),

    # wishlist page
    re_path(r'^ap/wish/list/page/captcha/bonus/list/$', views.ap_wishListPg_captcha_bonus_list, name='apWishListPgCaptchaBonusList'),
    re_path(r'^ap/remove/wish/list/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_wishListPage_captcha_bonus, name='ap_remove_wishListPage_captcha_bonus'),

    # credit purchase page
    re_path(r'^ap/credit/purchase/page/captcha/bonus/list/$', views.ap_creditPurchasePg_captcha_bonus_list, name='ap_creditPurchasePg_captcha_bonus_list'),
    re_path(r'^ap/remove/credit/purchase/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_creditPurchasePg_captcha_bonus, name='ap_remove_creditPurchasePg_captcha_bonus'),

    # credit purchase payment page
    re_path(r'^ap/credit/purchase/payment/page/captcha/bonus/list/$', views.ap_creditPurchasePaymntPg_captcha_bonus_list, name='ap_creditPurchasePaymntPg_captcha_bonus_list'),
    re_path(r'^ap/remove/credit/purchase/payment/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_creditPurchasePaymntPg_captcha_bonus, name='ap_remove_creditPurchasePaymntPg_captcha_bonus'),

    # check out page
    re_path(r'^ap/check/out/page/captcha/bonus/list/$', views.ap_checkOutPg_captcha_bonus_list, name='ap_checkOutPg_captcha_bonus_list'),
    re_path(r'^ap/remove/checkout/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_checkOutPg_captcha_bonus, name='ap_remove_checkOutPg_captcha_bonus'),

    # winning chance prchase success page
    re_path(r'^ap/winning/chance/purchase/success/page/captcha/bonus/list/$', views.ap_WinningChncePrchaseSuccessPg_captcha_bonus_list, name='ap_WinningChncePrchaseSuccessPg_captcha_bonus_list'),
    re_path(r'^ap/remove/checkout/page/captcha/bonus/(?P<pk>\d+)/$', views.ap_remove_WinningChncePrchaseSuccessPg_captcha_bonus, name='ap_remove_WinningChncePrchaseSuccessPg_captcha_bonus'),

    # prize section for analytics
    re_path(r'^ap/all/prizes/for/analytics/$', views.ap_all_prizesForAnalytics, name='apAllPrizesForAnalytics'),
    re_path(r'^ap/remove/prize/from/all/prizes/for/analytics/(?P<pk>\d+)/$', views.ap_remove_prizeFromAllPrizeAnalytics, name='apRemovePrizeFromAllPrizesForAnalytics'),

    # membership rank started*********************************************************************
    re_path(r'^ap/add/new/membership/rank/$', views.apAddNewMembershipRank, name='apAddNewMembershipRank'),
    re_path(r'^ap/update/new/membership/rank/(?P<rank_id>[-\w]+)/$', views.apUpdateMembershipRank, name='apUpdateMembershipRank'),
    re_path(r'^ap/remove/membership/rank/(?P<rank_id>[-\w]+)/$', views.apRemoveMembershipRank, name='apRemoveMembershipRank'),

    re_path(r'^ap/add/offer/products/to/different/ranked/members/$', views.apAddOfferProductsToDiffRankedMember, name='apAddOfferToDiffRankedMembers'),
    re_path(r'^ap/update/offer/products/to/different/ranked/members/(?P<pk>\d+)/$', views.apUpdateOfferProductsToDiffRankedMember, name='apUpdateOfferProductsToDiffRankedMember'),
    re_path(r'^ap/remove/offer/product/to/different/ranked/member/(?P<pk>\d+)/$', views.apRemoveOfferProductToDifferentRankedMember, name='apRemoveOfferProductToDifferentRankedMember'),

    # how it works section starts
    re_path(r'^ap/add/how/spin2win/works/$', views.ap_add_how_spinit2Win_works, name='apAddHowSpin2winWorks'),
    re_path(r'^ap/remove/how/spin2win/works/(?P<pk>\d+)/$', views.ap_delete_how_spinit2Win_works, name='apDeleteHowSpin2winWorks'),
    re_path(r'^ap/update/how/spin2win/works/(?P<pk>\d+)/$', views.ap_update_how_spinit2Win_works, name='apUpdateHowSpin2winWorks'),

    # shipping class starts **********************************************************
    re_path(r'^ap/add/shipping/class/$', views.ap_add_shippingClass, name='apAddShippingClass'),
    re_path(r'^ap/update/shipping/class/(?P<pk>\d+)/$', views.ap_update_shippingClass, name='apUpdateShippingClass'),
    re_path(r'^ap/remove/shipping/class/(?P<pk>\d+)/$', views.ap_remove_shippingClass, name='apRemoveShippingClass'),
    re_path(r'^ap/products/under/shipping/class/(?P<pk>\d+)/$', views.ap_productListByShippingClass, name='apProudctsUnderShippingClass'),

    # criteria
    re_path(r'^ap/add/product/weight/criteria/$', views.ap_add_productWeightCriteria, name='apAddProductWeightCriteria'),
    re_path(r'^ap/update/product/weight/criteria/(?P<pk>\d+)/$', views.ap_update_productWeightCriteria, name='apUpdateProductWeightCriteria'),
    re_path(r'^ap/remove/product/weight/criteria/(?P<pk>\d+)/$', views.ap_remove_productWeightCriteria, name='apRemoveProductWeightCriteria'),

    re_path(r'^ap/group/up/products/by/shipping/class/$', views.ap_group_up_productsByShippingClass, name='apGroupUpProductsByShippinigClass'),
    re_path(r'^ap/update/grouped/products/shipping/class/$', views.ap_updateGroupedProductsShippingClass, name='apupdateGroupedProductsShippingClass'),


    # ads script setting *****************************************************
    re_path(r'^ap/ads/script/setting/$', views.ap_ads_scriptSetting, name='ap_ads_scriptSetting'),
    re_path(r'^ap/remove/ads/script/(?P<pk>\d+)/$', views.ap_remove_ads_script, name='ap_remove_ads_script'),
    re_path(r'^ap/update/ads/script/(?P<pk>\d+)/$', views.ap_update_ads_script, name='ap_update_ads_script'),

]
