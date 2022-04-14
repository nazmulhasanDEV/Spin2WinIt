from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [

    # login-register
    re_path(r'^ap/register/updated/$', views.ap_RegisterSuperUser, name="apSuperAdminRegister"),
    re_path(r'^ap/login/updated/$', views.ap_loginSuperUser, name="apSuperAdminLogin"),
    re_path(r'^ap/logout/super/user/$', views.logoutSuperUser, name="apLogoutSuperUser"),

    re_path(r'^index/$', views.index, name="apIndex"),
    re_path(r'^ap/home/$', views.home, name="apHome"),
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
    re_path(r'^ap/del/woocmrce/product/(?P<pk>\d+)/$', views.ap_del_woocmmrce_prdct, name='apDelWoocmrceProduct'),
    re_path(r'^ap/woocommerce/store/product/list/$', views.ap_woocommerce_store_list, name='apWoocommerceStoreList'),
    re_path(r'^ap/woocommerce/product/details/(?P<pk>\d+)/$', views.ap_wcmrce_prdct_details, name='apWoocmrcePrdctDetails'),

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
    re_path(r'^ap/staff/accounts/list/$', views.ap_staff_accounts_list, name= 'apStaffAccountsList'),

    # site_setting section *******************************************************
    re_path(r'^ap/about/us/$', views.ap_about_us, name='apAboutUs'),
    re_path(r'^ap/del/about/us/(?P<pk>\d+)/$', views.ap_del_about_us, name='apDelAboutUs'),
    re_path(r'ap/edit/about/us/(?P<pk>\d+)/$', views.ap_edit_about_us, name='apEditAboutUs'),

    re_path(r'^ap/contact/us/$', views.ap_contact_us, name='apcontactUs'),
    re_path(r'^ap/edit/contact/us/(?P<pk>\d+)/$', views.ap_edit_contact_us, name='apEditContactUs'),
    re_path(r'^ap/del/contact/us/(?P<pk>\d+)/$', views.ap_del_contact_us, name='apDelContactUs'),

    # policy setting ***************************************************
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

    # banner section starts ****************************************************
    re_path(r'^ap/add/banner/$', views.ap_add_banner, name='apAddBanner'),
    re_path(r'^ap/banner/list/$', views.ap_banner_list, name='apBannerList'),
    re_path(r'^ap/update/banner/(?P<pk>\d+)/(?P<banner_id>[-\w]+)/$', views.ap_update_banner, name='apUpdateBannerInfo'),
    re_path(r'^ap/banner/(?P<pk>\d+)/(?P<banner_id>[-\w]+)/details/$', views.ap_banner_details, name='apBannerDetails'),
    re_path(r'^ap/del/banner/(?P<pk>\d+)/$', views.ap_del_banner, name='apDelBanner'),

    # logo section **********************************************
    re_path(r'^ap/add/logo/$', views.ap_add_site_logo, name='apAddSiteLogo'),
    re_path(r'^ap/del/site/logo/(?P<pk>\d+)/$', views.ap_del_site_logo, name='apDelSiteLogo'),

]
