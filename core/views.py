import json
import math
import threading
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from user.models import *
from verification.random_code_gen import rand_num_gen
from verification.email_threadings import EmailThreading
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from game.models import *
from adminPanel.models import *
from product.models import *
from advertisement.models import *
from .models import *
from django.core.paginator import Paginator, EmptyPage
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.crypto import get_random_string
from adminPanel.views import create_orderToWcmrceStore
from .get_visitor_info import get_or_countVisitorInfo

def get_User_ip(request):

    if request.method == 'GET':
        btn_id = request.GET.get('btn_id')

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        if btn_id == '1' and ip and DisclaimerAgreeDisagreeIPList.objects.filter(ip=ip).count() <= 0:
            user_ip_list = DisclaimerAgreeDisagreeIPList.objects.create(ip=ip, status=True)
        if btn_id == '2' and ip and DisclaimerAgreeDisagreeIPList.objects.filter(ip=ip).count() <= 0:
            user_ip_list = DisclaimerAgreeDisagreeIPList.objects.create(ip=ip, status=False)
    return redirect('frontEndHome')


def front_index(request):

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()

    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    product_cat_list = ProductCategory.objects.all()

    products = Product_list.objects.all()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user cart status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,


        'product_cat_list_all': product_cat_list,
        'product_list': products,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
    }

    return render(request,  'frontEnd/index.html', context)


def front_home(request):

    # saving/counting visitor informations
    get_or_count_visitor = threading.Thread(target=get_or_countVisitorInfo, args=[request.META.get('HTTP_X_FORWARDED_FOR'), request])
    get_or_count_visitor.start()

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # home page slider starts
    home_pg_mini_top_slidr = HomeMiniTopBanner.objects.filter(status=True)

    # home page bottom slider
    home_pg_bottom_slidr = HomeMiniBottomBanner.objects.filter(status=True)

    # home page main banner/slider
    main_banner_or_slider = BannerList.objects.all()

    product_cat_list_all = ProductCategory.objects.all()

    products = ProductList.objects.all()

    # checking disclaimer agreement of the current user's ip
    ip_exist = None
    if True:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            crrnt_ip = x_forwarded_for.split(',')[-1].strip()
            ip_exist = DisclaimerAgreeDisagreeIPList.objects.filter(ip=crrnt_ip).first()
        else:
            crrnt_ip = request.META.get('REMOTE_ADDR')
            ip_exist = DisclaimerAgreeDisagreeIPList.objects.filter(ip=crrnt_ip).first()

    # product category list which has at least one product
    product_catList_with_prodct = []
    for x in product_cat_list_all:
        if ProductList.objects.filter(Q(category=x) | Q(cat_name__icontains=x.name)):
            product_catList_with_prodct.append(x)


    # product subcategory
    product_subcats = ProductSubCategory.objects.all()

    cats_in_subcats = [] # category list which has at least one subcategory
    for subcat in product_subcats:
        if subcat.category.name in cats_in_subcats:
            pass
        else:
            cats_in_subcats.append(subcat.category.name)


    # filtered products by category and listing all the product by category which has at least one product
    product_list = []

    if product_cat_list_all:
        for cat in product_cat_list_all:
            current_cat_products = ProductList.objects.filter(Q(category=cat) | Q(cat_name__icontains=cat.name))[:6]
            product_list.extend(current_cat_products)

    # user cart status
    user_cart_status = None

    # user wishlist status
    user_wishlist_status = None

    total_amount = 0

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    context = {
        'ip_exist': ip_exist,
        'main_banner_or_slider' : main_banner_or_slider,
        'product_cat_list_all': product_cat_list_all,
        'product_cat_list' : product_catList_with_prodct,
        'cats_in_subcats' : cats_in_subcats,
        'product_subcats': product_subcats,
        'product_list' : product_list,
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,

        'home_pg_mini_top_slidr': home_pg_mini_top_slidr,
        'home_pg_bottom_slidr': home_pg_bottom_slidr,
    }

    return render(request, 'frontEnd/home.html', context)

# check box captcha solving for home page
@login_required(login_url='/fe/login/register')
def front_checkBoxCaptchaBonus(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = CheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = CheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = CheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# check box captcha solving for shop page
@login_required(login_url='/fe/login/register')
def front_ShopCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = ShopCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = ShopCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = ShopCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# check box captcha solving for shop page by category
@login_required(login_url='/fe/login/register')
def front_CategoryShopCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = CategoryShopCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = CategoryShopCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = CategoryShopCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# check box captcha solving for product details page
@login_required(login_url='/fe/login/register')
def front_ProductDetailsCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user = ProductDetailsCheckBoxCaptcha.objects.filter(Q(user=request.user) & Q(product_id=product_id)).last()
        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = ProductDetailsCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = ProductDetailsCheckBoxCaptcha.objects.create(user=request.user, product_id=product_id)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# check box captcha solving for game page
@login_required(login_url='/fe/login/register')
def front_GameCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = GameCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = GameCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = GameCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# check box captcha solving for user profile page
@login_required(login_url='/fe/login/register')
def front_UsrProfileCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = UsrProfileCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = UsrProfileCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = UsrProfileCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# check box captcha solving for purchase winning chance page
@login_required(login_url='/fe/login/register')
def front_BuyWinningChanceBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = BuyWinningChanceBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = BuyWinningChanceBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = BuyWinningChanceBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# check box captcha solving for cart page
@login_required(login_url='/fe/login/register')
def front_CartCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = CartCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = CartCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = CartCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# check box captcha solving for checkout page
@login_required(login_url='/fe/login/register')
def front_CheckoutCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = CheckoutCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = CheckoutCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = CheckoutCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# check box captcha solving for contact-us page
@login_required(login_url='/fe/login/register')
def front_ContactUsCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = ContactUsCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = ContactUsCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = ContactUsCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# check box captcha solving for payment page for purchasing winning chance page
@login_required(login_url='/fe/login/register')
def front_PaymentWinningChnceCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = PaymentWinningChnceCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = PaymentWinningChnceCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = PaymentWinningChnceCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# check box captcha solving for product purchase payment page
@login_required(login_url='/fe/login/register')
def front_ProductPurchaseCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = ProductPurchaseCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = ProductPurchaseCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = ProductPurchaseCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# checkbox captcha for payment success page after purchasing product
@login_required(login_url='/fe/login/register')
def front_ProdctPaymntSccssCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = ProdctPaymntSccssCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = ProdctPaymntSccssCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = ProdctPaymntSccssCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# checkbox captcha for wishlist
@login_required(login_url='/fe/login/register')
def front_WishlistCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = WishlistCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = WishlistCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = WishlistCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# checkbox captcha for purchase credit page
@login_required(login_url='/fe/login/register')
def front_PurchaseCreditCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = PurchaseCreditCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = PurchaseCreditCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = PurchaseCreditCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

# checkbox captcha for purchase credit payment page
@login_required(login_url='/fe/login/register')
def front_CreditPurchasePaymntCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = CreditPurchasePaymntCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = CreditPurchasePaymntCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = CreditPurchasePaymntCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# checkbox captcha for purchase credit payment success page
@login_required(login_url='/fe/login/register')
def front_CreditPurchaseSuccessCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = CreditPurchaseSuccessCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = CreditPurchaseSuccessCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = CreditPurchaseSuccessCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


# checkbox captcha for purchase credit payment success page
@login_required(login_url='/fe/login/register')
def front_WnChancePurchaseSccMsgCheckBoxCaptcha(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        user = WnChancePurchaseSccMsgCheckBoxCaptcha.objects.filter(user=request.user).last()

        if user:
            expired_date = user.created + timedelta(days=1)
            today = timezone.now()

            if today >= expired_date:
                # updating new one
                checkBox_captchaModel = WnChancePurchaseSccMsgCheckBoxCaptcha.objects.create(user=request.user)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 50
                    usr_point_wllt.save()
                    messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
            else:
                messages.warning(request, "You already got bonus! Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            # updating new one
            checkBox_captchaModel = WnChancePurchaseSccMsgCheckBoxCaptcha.objects.create(user=request.user)

            # user point wallet
            usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
            if usr_point_wllt:
                usr_point_wllt.available = int(usr_point_wllt.available) + 50
                usr_point_wllt.save()
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                usr_point_wallet = PointWallet.objects.create(user=request.user, available=50)
                messages.success(request, "Congratulations. You got 50 reward points as bonus.Try one day later to get bonus again!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/fe/login/register')
def front_invisibleCaptchaBonus(reqeust):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == "POST":
        feedback = request.POST.get('invisible_captcha')

        if feedback:
            usr = InvisibleFeedbackCaptcha.objects.filter(user=request.user).first()

            if usr:
                expired_date = user.created + timedelta(days=2)
                today = datetime.today()
                if today >= expired_date:
                    usr.delete()

                    # update with new value
                    invisible_cptcha_model = InvisibleFeedbackCaptcha.objects.create(user=request.user, feedback=feedback)

                    # user point wallet
                    usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                    if usr_point_wllt:
                        usr_point_wllt.available = int(usr_point_wllt.available) + 30
                        usr_point_wllt.save()
                    else:
                        usr_point_wallet = PointWallet.objects.create(user=request.user, available=30)
                else:
                    messages.warning(request, "You already got bonus! Try every two days later!")
                    return redirect('frontEndHome')

            else:
                # update with new value
                invisible_cptcha_model = InvisibleFeedbackCaptcha.objects.create(user=request.user, feedback=feedback)

                # user point wallet
                usr_point_wllt = PointWallet.objects.filter(user=request.user).first()
                if usr_point_wllt:
                    usr_point_wllt.available = int(usr_point_wllt.available) + 30
                    usr_point_wllt.save()
                else:
                    usr_point_wallet = PointWallet.objects.create(user=request.user, available=30)

    return redirect('frontEndHome')


def send__mail(email):
    email.send()
    return True

def front_loginRegister(request):

    site_logo = SiteLogo.objects.filter().first()

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        phone = request.POST['phone']
        # nid__card_no = request.POST['nid__card_no']
        user_role = request.POST['user_role']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if fname and lname and email and username and phone and user_role and password and password == confirm_password:
            try:
                if len(Account.objects.filter(email=email)) <= 0 or len(Account.objects.filter(username=username)) <= 0 or len(Account.objects.filter(phone_no=phone)) <= 0:
                    # # sending verification email with code*********************************
                    # verification__code = rand_num_gen(3)
                    #
                    # # save to verification code model by user
                    # verification_code_model = VerificationCode(user_email=email, code=verification__code)
                    # verification_code_model.save()
                    #
                    # request.session.flush() # removing current session data
                    # request.session['v_email'] = email
                    # request.session['v_code'] = verification__code
                    # request.session.set_expiry(300)
                    # saving user information after sending verification mail

                    user = Account.objects.create_user(email=email, username=username, phone_no=phone,
                                                       password=password)
                    if user_role == 'b_r':
                        user.is_buyer = True
                        user.save()
                    if user_role == 's_r':
                        user.is_seller = True
                        user.save()
                    user.fname = fname
                    user.lname = lname
                    # user.nid_no = nid__card_no
                    user.save()

                    verification_url = f'http://spinit2win.com/user/account/veirfication/{username}/{phone}'
                    subject = f"Verification code"
                    html_content = render_to_string('backEnd_superAdmin/verification_template.html',
                                                    context={'verification_url': verification_url})
                    email = EmailMessage(subject, html_content, to=[email])
                    email.content_subtype = 'html'
                    # email.send(fail_silently=False)
                    EmailThreading(email).start()
                    messages.success(request, "Verification link sent to your mail!")
                    return redirect('frontEndLoginRegister')
            except:
                # getting existing user without verification and deleting
                user = Account.objects.filter(email=email).first()
                now = timezone.now()
                expired_date = user.joined_at + timedelta(days=1)

                # delete user if does not verify in a specific time
                if user and now >= expired_date:
                    user.delete()

                    # creating new account
                    user = Account.objects.create_user(email=email, username=username, phone_no=phone,
                                                       password=password)
                    if user_role == 'b_r':
                        user.is_buyer = True
                        user.save()
                    if user_role == 's_r':
                        user.is_seller = True
                        user.save()
                    user.fname = fname
                    user.lname = lname
                    # user.nid_no = nid__card_no
                    user.save()

                    verification_url = f'http://spinit2win.com/user/account/veirfication/{username}/{phone}'
                    subject = f"Verification code"
                    html_content = render_to_string('backEnd_superAdmin/verification_template.html',
                                                    context={'verification_url': verification_url})
                    email = EmailMessage(subject, html_content, to=[email])
                    email.content_subtype = 'html'
                    # email.send(fail_silently=False)
                    EmailThreading(email).start()

                    messages.success(request, "Verification link sent to your mail!")
                    return redirect('frontEndLoginRegister')
                else:
                    messages.warning(request, "User already exist with these credentials! Check your mail to verify!")
                    return redirect('frontEndLoginRegister')


                messages.success(request, "Account already exists with these email or username Or email not may be found! Try again!")
                return redirect('frontEndLoginRegister')


    context = {
        'site_logo': site_logo,
    }

    return render(request, 'frontEnd/login-register.html', context)

def front_loginUser(request):

    site_logo = SiteLogo.objects.filter().first()

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        user_role = request.POST['user_role']
        password = request.POST['password']


        if email and username and user_role and password:
            try:
                remember_me = request.POST['remember_me']
                user = get_object_or_404(Account, email=email)
                if user and user.status == '1' and user.is_active == True:
                    authenticate_user = authenticate(request, email=email, password=password)
                    if authenticate_user is not None:
                        if remember_me:
                            request.session.set_expiry(3600)
                        if user.is_buyer:
                            login(request, authenticate_user)
                            return redirect('frontEndHome')
                        if user.is_seller:
                            login(request, authenticate_user)
                            return redirect('sellerDashboardHome', username=user.username)
                else:
                    messages.success(request, "User not found! Try again!")
                    return redirect('frontEndLoginRegister')
            except:
                user = get_object_or_404(Account, email=email)
                if user and user.status == '1' and user.is_active == True:
                    authenticate_user = authenticate(request, email=email, password=password)
                    if authenticate_user is not None:
                        request.session.flush()
                        request.session.set_expiry(300)
                        if user.is_buyer:
                            login(request, authenticate_user)
                            return redirect('frontEndHome')
                        if user.is_seller:
                            login(request, authenticate_user)
                            return redirect('sellerDashboardHome', username=user.username)

    context = {
        'site_logo': site_logo,
    }

    return render(request, 'frontEnd/login.html', context)

def front_search(request):

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    product_cat_list_all = ProductCategory.objects.all()

    if request.method == 'POST':
        product_category = request.POST.get('product_category')
        search_content = request.POST.get('search_content')

        if product_category and search_content:
            cat = ProductCategory.objects.filter(pk=product_category).first()
            search_result = ProductList.objects.filter(Q(category=cat) | Q(title__icontains=search_content))

            # total_obj_found = search_result.count()
            context = {
                'search_cat': cat,
                'search_content': search_content,
                'search_result' : search_result,
                'site_logo': site_logo,
                'product_cat_list_all': product_cat_list_all,
            }
            return render(request, 'frontEnd/search.html', context)

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        total_amount = 0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = total_amount + (float(x.product.price) * x.quantity)
                if x.product.product_type == 'mcp':
                    total_amount = total_amount + (x.product.new_price * x.quantity)

        # user cart status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        context = {
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,

            'total_amount': total_amount,
            'site_logo': site_logo,
            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'product_cat_list_all': product_cat_list_all,
        }
        return render(request, 'frontEnd/search.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'product_cat_list_all': product_cat_list_all,
    }

    return render(request, 'frontEnd/search.html', context)

def front_shop_for_all_category(request):

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # home page main banner/slider
    main_banner_or_slider = BannerList.objects.all()

    product_cat_list_all = ProductCategory.objects.all()

    products = ProductList.objects.all()

    # product category list which has at least one product
    product_catList_with_prodct = []
    for x in product_cat_list_all:
        if ProductList.objects.filter(Q(category=x) | Q(cat_name__icontains=x.name)):
            product_catList_with_prodct.append(x)

    # product subcategory
    product_subcats = ProductSubCategory.objects.all()

    cats_in_subcats = []  # category list which has at least one subcategory
    for subcat in product_subcats:
        if subcat.category.name in cats_in_subcats:
            pass
        else:
            cats_in_subcats.append(subcat.category.name)

    # filtered products by category and listing all the product by category which has at least one product
    product_list = []

    if product_cat_list_all:
        for cat in product_cat_list_all:
            current_cat_products = ProductList.objects.filter(Q(category=cat) | Q(cat_name__icontains=cat.name))[:5]
            product_list.extend(current_cat_products)

    if request.user.is_authenticated:

        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        total_amount = 0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = total_amount + (float(x.product.price) * x.quantity)
                if x.product.product_type == 'mcp':
                    total_amount = total_amount + (x.product.new_price * x.quantity)

        # user cart status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        context = {
            'main_banner_or_slider': main_banner_or_slider,
            'product_cat_list_all': product_cat_list_all,
            'product_cat_list': product_catList_with_prodct,
            'cats_in_subcats': cats_in_subcats,
            'product_subcats': product_subcats,
            'total_amount': total_amount,
            'product_list': product_list,
            'site_logo': site_logo,
            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,
        }
        return render(request, 'frontEnd/shop/shop_for_all_cats.html', context)

    context = {
        'main_banner_or_slider': main_banner_or_slider,
        'product_cat_list_all': product_cat_list_all,
        'product_cat_list': product_catList_with_prodct,
        'cats_in_subcats': cats_in_subcats,
        'product_subcats': product_subcats,
        'product_list': product_list,

        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }

    return render(request, 'frontEnd/shop/shop_for_all_cats.html', context)

def front_shop(request, pk):

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # current category by pk
    cat = ProductCategory.objects.get(pk=pk)

    # product list by current category
    products = ProductList.objects.filter(Q(category=cat) | Q(cat_name__icontains=cat.name))

    # shop page banner by category
    banner_at_shop_page_by_cat = ShopPageBanner.objects.filter(status=True).first()

    # django pagination
    paginator = Paginator(products, 8)

    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(1)


    # collecting user cart and wishlist status if authenticated
    total_amount = 0
    user_cart_status = None
    user_wishlist_status = None
    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)


        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = total_amount + (float(x.product.price) * x.quantity)
                if x.product.product_type == 'mcp':
                    total_amount = total_amount + (x.product.new_price * x.quantity)

        # user cart status
        user_wishlist_status = WishList.objects.filter(user=request.user)

    context = {
        'paginator' : paginator,
        'page' : page,
        'current_cat': cat,
        'total_amount': total_amount,
        'current_pk' : pk,
        'products': page,
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'banner_at_shop_page_by_cat': banner_at_shop_page_by_cat,
    }
    return render(request, 'frontEnd/shop/shop.html', context)

def front_productDetails(request, product_id):

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # advertisement banner
    prod_details_pg_bnr = BannerProdDetail.objects.filter(status=True).first()

    # current product
    current_product = ProductList.objects.get(product_id=product_id)

    # products of current category
    current_cat_product_list = ProductList.objects.filter(Q(category=current_product.category) | Q(cat_name=current_product.cat_name))[:8]

    # company refund polify
    refund_policy = RefundPolicy.objects.filter().first()
    return_policy = ReturnPolicy.objects.filter().first()
    security_policy = SecurityPolicy.objects.filter().first()
    delivery_policy = DeliveryPolicy.objects.filter().first()

    # ratings and reviews of current product
    current_prod_revs = ProductRating.objects.filter(product=current_product)

    num_of_5_star = 0
    num_of_4_star = 0
    num_of_3_star = 0
    num_of_2_star = 0
    num_of_1_star = 0
    # number of 5-star of current product
    if current_prod_revs.count() > 0:
        num_of_5_star = round(((ProductRating.objects.filter(Q(product=current_product) & Q(rating_val=5)).count()) / current_prod_revs.count()) * 100)
        num_of_4_star = round(((ProductRating.objects.filter(Q(product=current_product) & Q(rating_val=4)).count()) / current_prod_revs.count()) * 100)
        num_of_3_star = round(((ProductRating.objects.filter(Q(product=current_product) & Q(rating_val=3)).count()) / current_prod_revs.count()) * 100)
        num_of_2_star = round(((ProductRating.objects.filter(Q(product=current_product) & Q(rating_val=2)).count()) / current_prod_revs.count()) * 100)
        num_of_1_star = round(((ProductRating.objects.filter(Q(product=current_product) & Q(rating_val=1)).count()) / current_prod_revs.count()) * 100)


    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        total_amount = 0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = total_amount + (float(x.product.price) * x.quantity)
                if x.product.product_type == 'mcp':
                    total_amount = total_amount + (x.product.new_price * x.quantity)

        # user cart status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        context = {
            'total_amount' : total_amount,
            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,

            'current_product': current_product,
            'current_cat_product_list': current_cat_product_list,
            'refund_policy': refund_policy,
            'return_policy': return_policy,
            'security_policy': security_policy,
            'delivery_policy': delivery_policy,
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,

            'prod_details_pg_bnr': prod_details_pg_bnr,
            'current_prod_revs': current_prod_revs,
            'num_of_5_star': num_of_5_star,
            'num_of_4_star': num_of_4_star,
            'num_of_3_star': num_of_3_star,
            'num_of_2_star': num_of_2_star,
            'num_of_1_star': num_of_1_star,
        }
        return render(request, 'frontEnd/product-details.html', context)


    context = {
        'current_product' : current_product,
        'current_cat_product_list' : current_cat_product_list,
        'refund_policy' : refund_policy,
        'return_policy' : return_policy,
        'security_policy' : security_policy,
        'delivery_policy' : delivery_policy,
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'prod_details_pg_bnr': prod_details_pg_bnr,
        'current_prod_revs': current_prod_revs,

        'num_of_5_star': num_of_5_star,
        'num_of_4_star': num_of_4_star,
        'num_of_3_star': num_of_3_star,
        'num_of_2_star': num_of_2_star,
        'num_of_1_star': num_of_1_star,
    }

    return render(request, 'frontEnd/product-details.html', context)

@login_required(login_url='/fe/login/register')
def front_add_to_cart(request, product_id):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # getting current product
    current_product = ProductList.objects.get(product_id=product_id)

    if request.user.is_authenticated and current_product:
        if len(Cart.objects.filter(Q(user=request.user) & Q(product=current_product))) > 0:
            cart_model = Cart.objects.filter(Q(user=request.user) & Q(product=current_product)).first()

            cart_model.quantity = cart_model.quantity + 1
            cart_model.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product_cart_model = Cart(user=request.user, product=current_product, quantity=1)
            product_cart_model.save()
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/fe/login/register')
def front_remove_item_from_mini_cart(request, pk):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    try:
        # current product in cart
        current_product = Cart.objects.get(pk=pk)
        current_product.delete()
    except:
        pass

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/fe/login/register')
def front_cart_items_list(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True and len(Cart.objects.filter(user=request.user)) <= 0:
        return redirect('frontEndLoginRegister')

    if len(Cart.objects.filter(user=request.user)) <=0:
        return redirect('frontEndHome')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # ajax request part to handle increasing/decreasing product items from cart list

    product_id = request.GET.get('item_id')
    no_of_current_updated_items = request.GET.get('no_items')

    sub_total_amount = 0
    total_amount = 0

    if product_id and no_of_current_updated_items:
        # according to ajax request
        current_cart_item = Cart.objects.get(pk=product_id)

        if int(no_of_current_updated_items) <= 0:
            current_cart_item.delete()
        else:
            current_cart_item.quantity = int(no_of_current_updated_items)
            current_cart_item.save()

        updated_total_amount = 0

        # collecting updated total amount
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                updated_total_amount = round(updated_total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                updated_total_amount = round(updated_total_amount + (x.product.new_price * x.quantity), 2)

        updated_product_info = {
            'no_current_item': current_cart_item.quantity,
            'amount' : round(current_cart_item.total_amount, 2),
            'updated_total_amount': round(updated_total_amount, 2)
        }
        if request.is_ajax():
            return JsonResponse({'updated_product_info': updated_product_info})

    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                sub_total_amount = total_amount
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
                sub_total_amount = total_amount

    # user cart status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    product_cart_list = Cart.objects.filter(user=request.user)

    context = {
        'current_user_usrname': username,
        'product_cart_list': product_cart_list,
        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
        'sub_total_amount': sub_total_amount,

        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }

    return render(request, 'frontEnd/cart.html', context)

@login_required(login_url='/fe/login/register')
def front_checkout(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True and len(Cart.objects.filter(user=request.user)) <= 0:
        return redirect('frontEndLoginRegister')

    if len(Cart.objects.filter(user=request.user)) <=0:
        return redirect('frontEndHome')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user cart status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    # user default shipping address
    usr_deflt_shipping_addrss = DefalutShippingInfo.objects.filter(user=request.user).first()

    # user default billing address
    usr_deflt_billing_address = DefaultBillingInfo.objects.filter(user=request.user).first()

    total_amount = 0

    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
        'usr_deflt_shipping_addrss': usr_deflt_shipping_addrss,
        'usr_deflt_billing_address': usr_deflt_billing_address,
    }

    return render(request, 'frontEnd/checkout.html', context)


# send the order to woocommerce store

@login_required(login_url='/fe/login/register')
def front_confirm_order(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        # default shipping and billing address
        use_defalt_billing__adrs = request.POST.get('use_defalt_billin__adrs')
        use_defalt_shipping_addrss = request.POST.get('use_defalt_shipping_addrss')

        # billing informations
        country_b = request.POST.get('country_b')
        fname_b = request.POST.get('fname_b')
        lanme_b = request.POST.get('lanme_b')
        company_b = request.POST.get('company_b')
        address_b = request.POST.get('address_b')
        town_city_b = request.POST.get('town_city_b')
        state_b = request.POST.get('state_b')
        postcode_b = request.POST.get('postcode_b')
        email_b = request.POST.get('email_b')
        phone_b = request.POST.get('phone_b')

        # shipping info
        country_s = request.POST.get('country_s')
        fname_s = request.POST.get('fname_s')
        lanme_s = request.POST.get('lname_s')
        company_s = request.POST.get('company_s')
        address_s = request.POST.get('address_s')
        town_city_s = request.POST.get('town_city_s')
        state_s = request.POST.get('state_s')
        postcode_s = request.POST.get('postcode_s')
        email_s = request.POST.get('email_s')
        phone_s = request.POST.get('phone_s')

        order_note = request.POST.get('order_note')

        # random id generation for billing and shipping info
        id = uuid.uuid4()

        # user current cart items
        user_cart_items = Cart.objects.filter(user=request.user)

        if user_cart_items.count() <= 0:
            # grabing current user last order details
            current_order = OrderList.objects.filter(user=request.user).last()

            if current_order:
                return redirect('frontCompletePayment', username=request.user.username, order_id=current_order.order_id)
            else:
                return redirect('frontEndHome')

        else:
            try:
                # checking previous order items of the current user
                if len(OrderedItem.objects.filter(user=request.user)) > 0:
                    for item in OrderedItem.objects.filter(user=request.user):
                        item.order_status = 'prev'
                        item.save()

                # creating new order
                total_amount = 0
                # user order items
                for x in user_cart_items:
                    user_order_item = OrderedItem.objects.create(user=x.user, product=x.product, quantity=x.quantity,
                                                                 total_amount=x.total_amount, order_status='curnt')
                    total_amount = total_amount + float(x.total_amount)

                # saving billing informations

                if use_defalt_billing__adrs:
                    current_usr_billing_adrs = DefaultBillingInfo.objects.filter(user=request.user).first()

                    billing_info_model = BillingInfo.objects.create(
                        info_id=id,
                        user=request.user,
                        use_defalut_address=True,
                        default_billingAddress=current_usr_billing_adrs,
                    )
                else:
                    billing_info_model = BillingInfo.objects.create(
                        info_id=id,
                        user=request.user,
                        fname=fname_b,
                        lname=lanme_b,
                        country=country_b,
                        company=company_b,
                        address=address_b,
                        town_or_city=town_city_b,
                        state=state_b,
                        postcode=postcode_b,
                        email=email_b,
                        phone=phone_b
                    )

                # saving shipping informations
                if use_defalt_shipping_addrss:
                    current_usr_dflt_shipping_addrs = DefalutShippingInfo.objects.filter(user=request.user).first()
                    shipping_information_model = ShippingInfo.objects.create(
                        info_id=id,
                        user=request.user,
                        use_deflt_address=True,
                        default_shipping_address=current_usr_dflt_shipping_addrs,
                    )
                else:
                    shipping_information_model = ShippingInfo.objects.create(
                        info_id=id,
                        user=request.user,
                        fname=fname_s,
                        lname=lanme_s,
                        country=country_s,
                        company=company_s,
                        address=address_s,
                        town_or_city=town_city_s,
                        state=state_s,
                        postcode=postcode_s,
                        email=email_s,
                        phone=phone_s,
                    )

                # saving the order

                order_list_model = OrderList.objects.create(
                    order_id=id,
                    user=request.user,
                    order_status='a',
                    delivery_status=False,
                    billing_info=BillingInfo.objects.get(info_id=id),
                    shipping_info=ShippingInfo.objects.get(info_id=id),
                    order_note=order_note,
                    sub_total_amount=total_amount,
                    total_amount=total_amount,
                )
                for x in OrderedItem.objects.filter(Q(user=request.user) & Q(order_status='curnt')):
                    order_list_model.items.add(x)
                    x.order_status = 'curnt'
                    x.save()

                # sending order to woocommerce store
                order_data = None
                bill_fname = order_list_model.billing_info.fname
                bill_address_1 = order_list_model.billing_info.address
                bill_city = order_list_model.billing_info.town_or_city
                bill_state = order_list_model.billing_info.state
                bill_postcode = order_list_model.billing_info.postcode
                bill_country = order_list_model.billing_info.country
                bill_email = order_list_model.billing_info.email
                bill_phone = order_list_model.billing_info.phone

                ship_fname = order_list_model.shipping_info.email
                ship_address_1 = order_list_model.shipping_info.email
                ship_city = order_list_model.shipping_info.email
                ship_state = order_list_model.shipping_info.email
                ship_postcode = order_list_model.shipping_info.email
                ship_country = order_list_model.shipping_info.email
                ship_email = order_list_model.shipping_info.email
                ship_phone = order_list_model.shipping_info.email

                if order_list_model.billing_info.default_billingAddress:
                    bill_fname = order_list_model.billing_info.default_billingAddress.fname
                    bill_address_1 = order_list_model.billing_info.default_billingAddress.address
                    bill_city = order_list_model.billing_info.default_billingAddress.town_or_city
                    bill_state = order_list_model.billing_info.default_billingAddress.state
                    bill_postcode = order_list_model.billing_info.default_billingAddress.postcode
                    bill_country = order_list_model.billing_info.default_billingAddress.country
                    bill_email = order_list_model.billing_info.default_billingAddress.email
                    bill_phone = order_list_model.billing_info.default_billingAddress.phone

                if order_list_model.shipping_info.default_shipping_address:
                    ship_fname = order_list_model.shipping_info.default_shipping_address.fname
                    ship_address_1 = order_list_model.shipping_info.default_shipping_address.address
                    ship_city = order_list_model.shipping_info.default_shipping_address.town_or_city
                    ship_state = order_list_model.shipping_info.default_shipping_address.state
                    ship_postcode = order_list_model.shipping_info.default_shipping_address.postcode
                    ship_country = order_list_model.shipping_info.default_shipping_address.country
                    ship_email = order_list_model.shipping_info.default_shipping_address.email
                    ship_phone = order_list_model.shipping_info.default_shipping_address.phone

                order_data = {
                    "payment_method": "Paypal",
                    "payment_method_title": "Paypal",
                    "set_paid": True,
                    "billing": {
                        "first_name": str(bill_fname),
                        "last_name": "",
                        "address_1": str(bill_address_1),
                        "address_2": "",
                        "city": str(bill_city),
                        "state": str(bill_state),
                        "postcode": str(bill_postcode),
                        "country": str(bill_country),
                        "email": str(bill_email),
                        "phone": str(bill_phone),
                    },
                    "shipping": {
                        "first_name": str(ship_fname),
                        "last_name": "",
                        "address_1": str(ship_address_1),
                        "address_2": "",
                        "city": str(ship_city),
                        "state": str(ship_state),
                        "postcode": str(ship_postcode),
                        "country": str(ship_country)
                    },
                    "line_items": [
                        {'product_id': item.product.product_id, 'quantity': item.quantity} for item in order_list_model.items.all()
                    ],
                    "shipping_lines": [
                        {
                            "method_id": "flat_rate",
                            "method_title": "Flat Rate",
                            "total": str(order_list_model.total_amount)
                        }
                    ]
                }

                if order_data:
                    # create_orderToWcmrceStore(order_data)
                    order_send_thread = threading.Thread(target=create_orderToWcmrceStore, args=[order_data])
                    order_send_thread.start()

                # sending order to woocommerce store ends here

                # removing cart items after confirming order
                for cart in user_cart_items:
                    cart.delete()
                return redirect('frontCompletePayment', username=request.user.username, order_id=id)

            except:
                messages.warning(request, "Can't process your order! Try again please!")
                return redirect('frontEndCheckOut', username=request.user.username)

    return redirect('frontEndCheckOut', username=request.user.username)


@login_required(login_url='/fe/login/register')
def front_complete_payment(request, username, order_id):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if len(OrderList.objects.filter(user=request.user)) <=0:
        return redirect('frontEndHome')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()


    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)


    # grabing current user order details
    current_order = OrderList.objects.filter(order_id=order_id).first()

    # apply coupon code section
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        if coupon_code:
            coupon_code_model = CouponCode.objects.filter(coupon_code=coupon_code).first()
            if coupon_code_model:

                applied_coupon_history_model = AppliedCouponHistory.objects.filter(Q(order=current_order) & Q(coupon=coupon_code_model)).count()

                if coupon_code_model.status and applied_coupon_history_model <= 0:
                    discnt_amnt_got_applying_coupon = ((coupon_code_model.discount_amnt) * float(current_order.total_amount)) / 100  # Discount amount got after applying coupon code
                    current_order.total_amount = float(current_order.total_amount) - float(discnt_amnt_got_applying_coupon)
                    current_order.save()

                    # saving to coupon applied history
                    coupon_history_model = AppliedCouponHistory.objects.create(order=current_order, coupon=coupon_code_model, discount_got=discnt_amnt_got_applying_coupon)
                else:
                    messages.warning(request, "Invalid coupon code!")
                    return redirect('frontCompletePayment', username=request.user.username, order_id=current_order.order_id)


    if request.method == 'GET':
        # confirm payment
        paid_amount = request.GET.get('paid_amount')
        order_id = request.GET.get('order_id')

        if paid_amount and order_id:
            current_order.payment_status = True
            current_order.save()

            # update product total sold items
            # total_sold
            for item in current_order.items.all():
                productList__model = ProductList.objects.filter(pk=item.product.pk).first()
                productList__model.total_sold = productList__model.total_sold + item.quantity
                productList__model.save()

            # give user 1% reward point as bonus
            bonus_reward_point = (float(paid_amount) * 1) / 100
            # save to user wallet
            user_wallet = PointWallet.objects.filter(user=request.user).first()
            if user_wallet:
                user_wallet.available = int(user_wallet.available) + math.ceil(bonus_reward_point)
                user_wallet.save()
            else:
                user_wallet = PointWallet.objects.create(user=request.user, available=math.ceil(bonus_reward_point))

            return redirect('frontPaymentSuccessfullmsg', username=request.user.username)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,


        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
        'current_order' : current_order,
    }

    return render(request, 'frontEnd/payment.html', context)


@login_required(login_url='/fe/login/register')
def front_buy_now(request, product_id):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        price = float(request.POST.get('product_price'))

        if quantity and product_id:
            product = ProductList.objects.get(product_id=product_id)
            cart_model = Cart.objects.create(user=request.user, product=product, quantity=quantity)

            return redirect('frontEndCheckOut', username=request.user.username)

    return render(request, 'frontEnd/buy_now.html')

@login_required(login_url='/fe/login/register')
def front_leave_product_review(request, product_id):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    current_product = ProductList.objects.get(product_id=product_id)

    if request.method == 'POST':
        ratin_val = request.POST.get('ratin_val')
        comment = request.POST.get('comment')

        if ratin_val and comment:
            if ProductRating.objects.filter(Q(user=request.user) & Q(product=current_product)).count() > 0:
                messages.warning(request, "You already left a feedback!")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                product_rev_model = ProductRating.objects.create(user=request.user, product=current_product, rating_val=int(ratin_val), comment=comment)

                # total number review of current product
                total_num_of_rev = ProductRating.objects.filter(product=current_product).count()

                # average rating value
                avg = ProductRating.objects.filter(product=current_product).aggregate(Avg('rating_val'))

                # update the current product review and average
                current_product.avrg_rating = avg['rating_val__avg']
                current_product.rating_count = total_num_of_rev
                current_product.save()


                messages.success(request, "Thanks for your feedback!")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/fe/login/register')
def front_add_to_wishlist(request, product_id):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # getting current product
    current_product = ProductList.objects.get(product_id=product_id)

    if request.user.is_authenticated and current_product:
        if len(WishList.objects.filter(Q(user=request.user) & Q(product=current_product))) > 0:
            wishlist_model = WishList.objects.filter(Q(user=request.user) & Q(product=current_product)).first()

            wishlist_model.quantity = wishlist_model.quantity + 1
            wishlist_model.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product_wishlist_model = WishList(user=request.user, product=current_product, quantity=1)
            product_wishlist_model.save()
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/fe/login/register')
def front_wishlist(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
    }

    return render(request, 'frontEnd/wishlist.html', context)


@login_required(login_url='/fe/login/register')
def front_remove_item_from_wishlist(request, username, pk):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    current_wishlist = WishList.objects.get(pk=pk)
    current_wishlist.delete()

    return redirect('frontWishlist', username=request.user.username)


def front_game(request):

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # grabing sponsored product sponsored product
    sponsored_product = SponsoredProductForPrize.objects.filter(status=True).first()

    # applicable rules for sponsored product
    applicable_rules = None
    if sponsored_product:
        applicable_rules = ApplicableRulesForWinner.objects.filter(product=sponsored_product).first()

    if request.user.is_authenticated:

        # segment with gold, silver, Diamond price
        gold_prize_cost = 0
        gold_prize_necessaary_spins = 0
        gold_prize = SegmentList.objects.filter(prize_title='Gold').first()
        if gold_prize:
            if gold_prize.product_as_prize.product.product_type == 'wsp':
                gold_prize_cost = gold_prize.product_as_prize.product.price
                gold_prize_necessaary_spins = math.ceil(float(gold_prize_cost) / (.10)) # here .10 cent == 1 spin
            else:
                gold_prize_cost = gold_prize.product_as_prize.product.new_price
                gold_prize_necessaary_spins = math.ceil(float(gold_prize_cost) / (.10)) # here .10 cent == 1 spin

        silver_prize = SegmentList.objects.filter(prize_title='Silver').first()
        silver_prize_cost = 0
        silver_prize_necessaary_spins = 0

        if silver_prize:
            if silver_prize.product_as_prize.product.product_type == 'wsp':
                silver_prize_cost = silver_prize.product_as_prize.product.price
                silver_prize_necessaary_spins = math.ceil(float(silver_prize_cost) / (.10))  # here .10 cent == 1 spin
            else:
                silver_prize_cost = gold_prize.product_as_prize.product.new_price
                silver_prize_necessaary_spins = math.ceil(float(silver_prize_cost) / (.10))  # here .10 cent == 1 spin
        # for bronze prize
        bronze_prize = SegmentList.objects.filter(prize_title='Bronze').first()
        bronze_prize_cost = 0
        bronze_prize_necessaary_spins = 0

        if bronze_prize:
            if bronze_prize.product_as_prize.product.product_type == 'wsp':
                bronze_prize_cost = bronze_prize.product_as_prize.product.price
                # gold_prize_necessaary_spins = math.ceil(float(gold_prize_cost) / (.10)) # here .10 cent == 1 spin
                bronze_prize_necessaary_spins = math.ceil(float(bronze_prize_cost) / (.10)) # here .10 cent == 1 spin
            else:
                bronze_prize_cost = bronze_prize.product_as_prize.product.new_price
                # gold_prize_necessaary_spins = math.ceil(float(bronze_prize_cost) / (.10))  # here .10 cent == 1 spin
                bronze_prize_necessaary_spins = math.ceil(float(bronze_prize_cost) / (.10))  # here .10 cent == 1 spin

        # getting current spinning chances
        current_chances = request.GET.get('current_chances')

        # getting request from restart spin
        fromRestartSpin = request.GET.get('fromRestartSpin')

        if fromRestartSpin:
            totalNumberOfTimesPlayedModel = TotalNumOfTimesPlayed.objects.filter().first()
            totalNumberOfTimesPlayedModel.num_of_times_played = int(totalNumberOfTimesPlayedModel.num_of_times_played) - 1
            totalNumberOfTimesPlayedModel.save()

            if request.is_ajax():
                current_total_num_of_played = TotalNumOfTimesPlayed.objects.filter().first()
                return JsonResponse({'current_total_num_of_played': current_total_num_of_played.num_of_times_played})

        # getting user
        user_winning_chances = WinningChance.objects.filter(user=request.user)

        user_total_remaining_chances = 0
        if user_winning_chances:
            if current_chances:
                # saving updated chances
                user_winning_chance_model = WinningChance.objects.get(user=request.user)
                user_winning_chance_model.remaining_chances = current_chances
                user_winning_chance_model.save()

            user_total_remaining_chances = user_total_remaining_chances + int(user_winning_chances.first().remaining_chances)

        # current chances sections
        if current_chances:
            total_number_of_times_played = TotalNumOfTimesPlayed.objects.filter().count()
            if total_number_of_times_played <= 0:
                total_num_of_times_played_model = TotalNumOfTimesPlayed.objects.create(num_of_times_played=1)
            else:
                total_num_of_times_played_model = TotalNumOfTimesPlayed.objects.filter().first()
                total_num_of_times_played_model.num_of_times_played = total_num_of_times_played_model.num_of_times_played + 1
                total_num_of_times_played_model.save()

                if request.is_ajax():
                    current_total_num_of_played = TotalNumOfTimesPlayed.objects.filter().first()
                    return JsonResponse({'current_total_num_of_played': current_total_num_of_played.num_of_times_played})



        # grabing user won prize
        won_prize = request.GET.get('won_prize')

        # converting won prize text into array
        last_str_of_won_prize = str(won_prize).split()[-1]

        if won_prize:
            # checking if the won prize is a point
            is_point = any(s.isdigit() for s in won_prize)

            if is_point:
                user_prize_list_model = PrizeList(user=request.user, prize_type='point', pirze=won_prize)
                user_prize_list_model.save()

                # UPDATE USER SPIN POINT WALLET
                usr_spin_point_wallet = PointWallet.objects.filter(user=request.user).first()
                if usr_spin_point_wallet:
                    usr_spin_point_wallet.available = int(usr_spin_point_wallet.available) + int(won_prize)
                    usr_spin_point_wallet.save()
            # checking if the won prize is a point ends *******************************************

            # checking if the won prize is a product
            segments_with_won_product = SegmentList.objects.filter(Q(segment_prize_type='1') & Q(prize_title__icontains=last_str_of_won_prize) & Q(status=True)).first()

            if segments_with_won_product:
                # getting won product informations
                won_product_id = segments_with_won_product.product_as_prize.product.product_id
                won_product = ProductList.objects.filter(product_id=won_product_id).first()
                user_prize_list_model = PrizeList(
                    user=request.user,
                    prize_type='product',
                    product_as_prize=won_product
                )
                user_prize_list_model.save()

        # grabing game settings
        game_setting = GameSetting.objects.filter(status=True).first()

        number_of_segments = len(SegmentList.objects.filter(status=True))
        active_segment_list = SegmentList.objects.filter(status=True)


        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,

            'sponsored_product' : sponsored_product,
            'applicable_rules': applicable_rules,
            'gold_prize_necessaary_spins': gold_prize_necessaary_spins,
            'silver_prize_necessaary_spins': silver_prize_necessaary_spins,
            'bronze_prize_necessaary_spins': bronze_prize_necessaary_spins,

            'user_total_remaining_chances' : user_total_remaining_chances,
            'game_setting': game_setting,
            'active_segment_list' : active_segment_list,
            'number_of_segments' : number_of_segments,
        }

        return render(request, 'frontEnd/game.html', context)

    # grabing game settings for unauthenticated user
    game_setting = GameSetting.objects.filter(status=True)

    context = {
        'game_setting' : game_setting,
        'site_logo' : site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'sponsored_product': sponsored_product,
        'applicable_rules' : applicable_rules,
    }
    return render(request, 'frontEnd/game.html', context)

@login_required(login_url='/fe/login/register')
def front_buy_winning_chance(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    user = Account.objects.get(email=request.user.email)

    # user point wallet
    point_wallet = PointWallet.objects.filter(user=request.user).first()

    # usr credit wallet
    usr_credit_wllet = CreditWallet.objects.filter(user=request.user).first()

    # ajax part starts ***********************************************
    number_of_winnging_chance = request.GET.get('winning_chance_number')
    if request.is_ajax():
        return JsonResponse({'number_of_winnging_chance' : number_of_winnging_chance})


    if request.method == 'POST':
        number_of_winning_chance = request.POST.get('number_of_winning_chance')
        credit_point_to_be_charged = request.POST.get('point_to_be_charged')

        if number_of_winning_chance and credit_point_to_be_charged:
            user_credit_point_wallet = CreditWallet.objects.filter(user=request.user).first()

            # asumptions: $1 = 2 credits, 100 points = 1 credit

            if user_credit_point_wallet and user_credit_point_wallet.available:
                if int(user_credit_point_wallet.available) >= int(credit_point_to_be_charged):
                    if len(WinningChance.objects.filter(user=request.user)) > 0:
                        user_winning_chance_model = WinningChance.objects.get(user=request.user)
                        user_winning_chance_model.remaining_chances = int(user_winning_chance_model.remaining_chances) + int(number_of_winning_chance)
                        user_winning_chance_model.save()

                        # updating point wallet after buying
                        user_credit_point_wallet.available = int(user_credit_point_wallet.available) - int(credit_point_to_be_charged)
                        user_credit_point_wallet.save()

                        # save to user purchase history
                        user_winning_change_prchase_history_model = WinningChancePurchasingHistory.objects.create(
                            user=request.user,
                            point_charged = credit_point_to_be_charged,
                            chance_purchased= number_of_winning_chance
                        )

                        # sending details to buyer/payer email
                        subject = f"Winning Chance Purchase Details"

                        paymentID = None
                        paid_amount = None
                        payer_name = None
                        payer_email = None
                        payer_id = None
                        payer_post_code = None
                        payer_country_code = None

                        context_info = {
                            'number_of_winning_chance': number_of_winning_chance,
                            'credit_point_to_be_charged': credit_point_to_be_charged,

                            'paymentID': paymentID,
                            'paid_amount': paid_amount,
                            'payer_name': payer_name,
                            'payer_email': payer_email,
                            'payer_id': payer_id,
                            'payer_post_code': payer_post_code,
                            'payer_country_code': payer_country_code,
                        }
                        html_content = render_to_string('frontEnd/buy_winning_chance/winning_chnce_purchase_cnfrm_mail.html',
                                                        context_info)
                        email = EmailMessage(subject, html_content, to=[request.user.email])
                        email.content_subtype = 'html'
                        EmailThreading(email).start()

                        messages.success(request, "Successfully bought new chances!")
                        return redirect('frontEndUserProfile', username=request.user.username)
                    else:
                        user_winning_chance_model = WinningChance(user=request.user,
                                                                  remaining_chances=number_of_winning_chance)
                        user_winning_chance_model.save()

                        # updating point wallet after buying
                        user_credit_point_wallet.available = int(user_credit_point_wallet.available) - int(credit_point_to_be_charged)
                        user_credit_point_wallet.save()

                        # save to user purchase history
                        user_winning_change_prchase_history_model = WinningChancePurchasingHistory.objects.create(
                            user=request.user,
                            point_charged=credit_point_to_be_charged,
                            chance_purchased=number_of_winning_chance
                        )

                        # sending details to payer email
                        subject = f"Winning Chance Purchase Details"

                        paymentID = None
                        paid_amount = None
                        payer_name = None
                        payer_email = None
                        payer_id = None
                        payer_post_code = None
                        payer_country_code = None

                        context_info = {
                            'number_of_winning_chance': number_of_winning_chance,
                            'credit_point_to_be_charged': credit_point_to_be_charged,

                            'paymentID': paymentID,
                            'paid_amount': paid_amount,
                            'payer_name': payer_name,
                            'payer_email': payer_email,
                            'payer_id': payer_id,
                            'payer_post_code': payer_post_code,
                            'payer_country_code': payer_country_code,
                        }
                        html_content = render_to_string('frontEnd/buy_winning_chance/winning_chnce_purchase_cnfrm_mail.html',context_info)
                        email = EmailMessage(subject, html_content, to=[request.user.email])
                        email.content_subtype = 'html'
                        EmailThreading(email).start()

                        messages.success(request, "Successfully bought new chances!")
                        return redirect('frontEndUserProfile', username=request.user.username)
                else:
                    # current available credits
                    available__credit_points = int(user_credit_point_wallet.available)

                    # finding lack of points to buy chance
                    lack_of_credit_points = int(credit_point_to_be_charged) - available__credit_points

                    # payable amount for buying chance for lack of points
                    payable_amount = (lack_of_credit_points) * (0.5)


                    context = {
                        'payable_amount' : payable_amount,
                        'available_points': available__credit_points,
                        'necessary_points' : credit_point_to_be_charged,
                        'winning_chance' : number_of_winning_chance,

                        'site_logo': site_logo,
                        'contact_info': contact_info,
                        'free_delivery_content_setting': free_delivery_content_setting,
                        'safe_payment_content_setting': safe_payment_content_setting,
                        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
                        'help_center_content_setting': help_center_content_setting,

                        'user_cart_status': user_cart_status,
                        'user_wishlist_status': user_wishlist_status,
                        'total_amount': total_amount,
                    }

                    return render(request, 'frontEnd/pay_for_purchasing_wnning_chance.html', context)
            else:
                payable_amount = int(credit_point_to_be_charged) * (0.5)

                context = {
                    'payable_amount': payable_amount,
                    'available_points': 0,
                    'necessary_points' : credit_point_to_be_charged,
                    'winning_chance': number_of_winning_chance,

                    'site_logo': site_logo,
                    'user_cart_status': user_cart_status,
                    'user_wishlist_status': user_wishlist_status,
                    'total_amount': total_amount,
                }

                return render(request, 'frontEnd/pay_for_purchasing_wnning_chance.html', context)

    context = {
        # 'game_setting': game_setting,
        'point_wallet' : point_wallet,
        'usr_credit_wllet': usr_credit_wllet,
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
    }

    return render(request, 'frontEnd/buy_winning_chance.html', context)

@login_required(login_url='/fe/login/register')
def front_pay_for_purchasing_wnning_chance(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    # user payment status
    if request.method == 'GET':

        paid_amount = request.GET.get('paid_amount')
        purchased_chances = request.GET.get('purchased_chances')
        necessary_points = request.GET.get('necessary_points')
        available_credit_points = request.GET.get('available_points')
        order_data = request.GET.get('order_data')


        if paid_amount and purchased_chances and necessary_points:

            # order_data
            orderData = json.loads(order_data)
            paymentID = orderData['id']

            # payee info
            payee_email = orderData['purchase_units'][0]['payee']['email_address']
            payee_marchnt_id = orderData['purchase_units'][0]['payee']['merchant_id']

            # payer info
            payer_name = orderData['payer']['name']['given_name'] + ' ' + orderData['payer']['name']['surname']
            payer_email = orderData['payer']['email_address']
            payer_id = orderData['payer']['payer_id']
            payer_post_code = orderData['payer']['address']['postal_code']
            payer_country_code = orderData['payer']['address']['country_code']

            usr_credit_wallet = CreditWallet.objects.filter(user=request.user).first()

            if usr_credit_wallet:
                usr_credit_wallet.available = '0'
                usr_credit_wallet.spent = int(usr_credit_wallet.spent) + int(available_credit_points)
                usr_credit_wallet.save()

            # user winning chance model
            winning_chance_model = WinningChance.objects.filter(user=request.user).first()

            # user credit point model
            usr_credit_point_model = CreditWallet.objects.filter(user=request.user).first()

            if winning_chance_model:
                winning_chance_model.remaining_chances = int(winning_chance_model.remaining_chances) + int(purchased_chances)
                winning_chance_model.save()
            if winning_chance_model is None:
                winning_chance_model = WinningChance.objects.create(user=request.user, remaining_chances=purchased_chances)


            # usr winning chance buying history
            winning_chance_buying_history_model = WinningChancePurchasingHistory.objects.create(
                user=request.user,
                point_charged=available_credit_points,
                amount_paid=paid_amount,
                chance_purchased=purchased_chances,
                payment_id=paymentID,
                payee_email=payee_email,
                payee_marchnt_id=payee_marchnt_id,
                payer_name=payer_name,
                payer_email=payer_email,
                payer_id=payer_id,
                payer_post_code=payer_post_code,
                payer_country_code=payer_country_code,
            )

            # sending details to buyer/payer email
            subject = f"Winning Chance Purchase Details"

            context_info = {
                'number_of_winning_chance': purchased_chances,
                'credit_point_to_be_charged': available_credit_points,

                'paymentID': paymentID,
                'paid_amount': paid_amount,
                'payer_name': payer_name,
                'payer_email': payer_email,
                'payer_id': payer_id,
                'payer_post_code': payer_post_code,
                'payer_country_code': payer_country_code,
            }
            html_content = render_to_string('frontEnd/buy_winning_chance/winning_chnce_purchase_cnfrm_mail.html',context_info)
            email = EmailMessage(subject, html_content, to=[request.user.email])
            email.content_subtype = 'html'
            EmailThreading(email).start()

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
    }

    return render(request, 'frontEnd/pay_for_purchasing_wnning_chance.html', context)

@login_required(login_url='/fe/login/register')
def front_winning_chance_purchasing_succss_msg(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
    }

    return render(request, 'frontEnd/buy_winning_chance/success_msg.html', context)


@login_required(login_url='/fe/login/register')
def front_payment_successfull_msg(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
    }

    return render(request, 'frontEnd/payment_successfull_msg.html', context)


# buy credit ****************************************
@login_required(login_url='/fe/login/register')
def front_buy_credit_point(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    # available credits
    user_available_credits = CreditWallet.objects.filter(user=request.user).first()

    # available points
    usr_available_points = PointWallet.objects.filter(user=request.user).first()

    # ajax part starts for buying credit points ***********************************************
    # assuming 1 credit point = $0.10
    credit_amount = request.GET.get('credit_amount')
    if request.is_ajax():
        return JsonResponse({'credit_amount': credit_amount})

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    if request.method == 'POST':
        credit__amount = request.POST.get('credit__point__amount')
        amount_to_be_charged = request.POST.get('amount_to_be_charged')

        # current user credit wallet
        crnt_user_credit_wallet = CreditWallet.objects.filter(user=request.user).first()

        context = {
            'credit__amount': credit__amount,
            'amount_to_be_charged': amount_to_be_charged,
            'crnt_user_credit_wallet': crnt_user_credit_wallet,
        }
        return render(request, 'frontEnd/credit/payment.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
        'username': username,
        'user_available_credits': user_available_credits,
        'usr_available_points': usr_available_points,
    }

    return render(request, 'frontEnd/credit/buy_credit.html', context)


@login_required(login_url='/fe/login/register')
def front_pay_for_purchasing_point(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')


    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    if request.method == 'GET':
        paid_amount = request.GET.get('paid_amount')
        credit__amount = request.GET.get('credit__amount')
        order_data = request.GET.get('order_data')

        if paid_amount and credit__amount and order_data:
            orderData = json.loads(order_data)

            paymentID = orderData['id']

            # payee info
            payee_email = orderData['purchase_units'][0]['payee']['email_address']
            payee_marchnt_id = orderData['purchase_units'][0]['payee']['merchant_id']

            # payer info
            payer_name = orderData['payer']['name']['given_name'] + ' ' + orderData['payer']['name']['surname']
            payer_email = orderData['payer']['email_address']
            payer_id = orderData['payer']['payer_id']
            payer_post_code = orderData['payer']['address']['postal_code']
            payer_country_code = orderData['payer']['address']['country_code']

            # user credit wallet
            user_credit_wallet = CreditWallet.objects.filter(user=request.user).first()

            if user_credit_wallet:
                user_credit_wallet.available = int(user_credit_wallet.available) + int(credit__amount)
                user_credit_wallet.save()

                # save payment details to credit purchase history
                usr_credit_purchase_history = CreditPurchasingHistory.objects.create(
                    user=request.user,
                    purchased_credit_amnt=credit__amount,
                    paid_amount=paid_amount,
                    payment_id=paymentID,
                    payee_email=payee_email,
                    payee_marchnt_id=payee_marchnt_id,

                    payer_name=payer_name,
                    payer_email=payer_email,
                    payer_id=payer_id,
                    payer_post_code=payer_post_code,
                    payer_country_code=payer_country_code,
                )

                # print(f'PaymentID: {paymentID}')
                # print(f'Payee email: {payee_email}')
                # print(f'Payee marchantID: {payee_marchnt_id}')
                # print(f'Payer Namae: {payer_name}')
                # print(f'Payer email: {payer_email}')
                # print(f'Payer id: {payer_id}')
                # print(f'Payer post code: {payer_post_code}')
                # print(f'Payer country code: {payer_country_code}')

                # sending details to payer email
                subject = f"Credit Purchase Details"

                context_info = {
                    'paymentID': paymentID,
                    'paid_amount': paid_amount,
                    'credit__amount': credit__amount,
                    'payer_name': payer_name,
                    'payer_email': payer_email,
                    'payer_id': payer_id,
                    'payer_post_code': payer_post_code,
                    'payer_country_code': payer_country_code,
                }
                html_content = render_to_string('frontEnd/credit/credit_purchase_cnfirm_mail.html', context_info)
                email = EmailMessage(subject, html_content, to=[request.user.email])
                email.content_subtype = 'html'
                EmailThreading(email).start()

            else:
                usr_credit_wallet = CreditWallet.objects.create(user=request.user, available=credit__amount)

                # save payment details to credit purchase history
                usr_credit_purchase_history = CreditPurchasingHistory.objects.create(
                    user=request.user,
                    purchased_credit_amnt=credit__amount,
                    paid_amount=paid_amount,
                    payment_id=paymentID,
                    payee_email=payee_email,
                    payee_marchnt_id=payee_marchnt_id,

                    payer_name=payer_name,
                    payer_email=payer_email,
                    payer_id=payer_id,
                    payer_post_code=payer_post_code,
                    payer_country_code=payer_country_code,
                )

                # sending details to payer email
                subject = f"Credit Purchase Details"
                context_info = {
                    'paymentID': paymentID,
                    'paid_amount': paid_amount,
                    'credit__amount': credit__amount,
                    'payer_name': payer_name,
                    'payer_email': payer_email,
                    'payer_id': payer_id,
                    'payer_post_code': payer_post_code,
                    'payer_country_code': payer_country_code,
                }
                html_content = render_to_string('frontEnd/credit/credit_purchase_cnfirm_mail.html', context_info)
                email = EmailMessage(subject, html_content, to=[request.user.email])
                email.content_subtype = 'html'
                EmailThreading(email).start()

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
    }
    return render(request, 'frontEnd/credit/payment.html', context)

@login_required(login_url='/fe/login/register')
def fron_credit_purchase_success_msg(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # site logo
    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
    }

    return render(request, 'frontEnd/credit/success_msg.html', context)


# ends buy credit point section
def front_give_email_to_reset_pass(request):

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        user_role = request.POST.get('user_role')
        try:
            user = Account.objects.get(email=email)
            if user:
                # provide permission to reset password
                reset_permission_model = ResetPermissionStatus(user=user, status='1')
                reset_permission_model.save()

                # send reset password link
                verification_url = f'http://127.0.0.1:8000/fe/reset/password/{username}'
                subject = f"Reset Password"
                html_content = render_to_string('verification/reset_password_link.html',
                                                context={'verification_url': verification_url})
                email = EmailMessage(subject, html_content, to=[email])
                email.content_subtype = 'html'
                EmailThreading(email).start()

                messages.success(request, "Reset password link has been sent to your email!")
                return redirect('frontGiveEmailResetPassword')
        except:
            messages.warning(request, "User not found with this email! Try again!")
            return redirect('frontGiveEmailResetPassword')

    context = {
        'game_setting': game_setting,
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }

    return render(request, 'verification/email_for_forgot_pass.html', context)

def front_reset_password(request, username):

    if Account.objects.filter(username=username):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_pass = request.POST.get('confirm_password')

            if email and password and confirm_pass:
                try:
                    user = Account.objects.get(email=email)
                    if password == confirm_pass:
                        user.set_password(password)
                        user.save()
                        messages.success(request, "Your password has been changed!")
                        return redirect('frontEndLoginUser')
                    else:
                        messages.warning(request, "Password didn't match! Try again!")
                        return redirect('frontEndLoginUser')
                except:
                    messages.warning(request, "User not found with this email! Try again!")
                    return redirect('frontEndLoginUser')
        # permit_user_for_reset_pass = ResetPermissionStatus
    else:
        messages.warning(request, "Account not found!")
        return redirect('frontEndHome')

    context = {
        'username' : username,
    }

    return render(request, 'verification/reset_password.html', context)


# user profile section ********************************************************
@login_required(login_url='/fe/login/register')
def front_user_profile(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user profile pic
    user_profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # user points wallet
    user_point_wallet = PointWallet.objects.filter(user=request.user).first()

    # user credit wallet
    user_credit_wallet = CreditWallet.objects.filter(user=request.user).first()

    # user winning chances
    user_winning_chances = WinningChance.objects.filter(user=request.user).first()

    # user orders
    order_list = OrderList.objects.filter(user=request.user).filter()

    # user default shipping address
    user_dflt_shipping_address = DefalutShippingInfo.objects.filter(user=request.user).first()

    # usr default billing address
    usr_default_biling_address = DefaultBillingInfo.objects.filter(user=request.user).first()

    # user prize list
    usr_won_prize_list = PrizeList.objects.filter(user=request.user)

    # all product category
    product_cat_list_all = ProductCategory.objects.all()

    # ads list on user profile
    user_profile_ads_list = UserProfileAds.objects.filter(status=True)

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)


    context = {
        'username' : username,
        'order_list' : order_list,
        'user_profile_pic' : user_profile_pic,
        'user_point_wallet' : user_point_wallet,
        'user_credit_wallet': user_credit_wallet,
        'user_winning_chances' : user_winning_chances,

        'user_dflt_shipping_address': user_dflt_shipping_address,
        'usr_default_biling_address': usr_default_biling_address,
        'usr_won_prize_list': usr_won_prize_list,
        'user_profile_ads_list': user_profile_ads_list,
        'product_cat_list_all': product_cat_list_all,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,

        'site_logo' : site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }
    return render(request, 'frontEnd/user_profile.html', context)


# user prize cart and delivery section *******************************************************
@login_required(login_url='/fe/login/register')
def front_move_prizes_toPrizeCart(request, product_id, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    try:
        current_product = ProductList.objects.filter(product_id=product_id).first()

        # current prize
        if current_product:
            current_prize = PrizeList.objects.filter(Q(product_as_prize=current_product) & Q(user=request.user)).first()
            current_prize.status = True
            current_prize.save()

            # save the current prize product to prize cart
            save_to_prize_cart = PrizeCart.objects.create(user=request.user, product=current_product)
            messages.success(request, "Your prize moved to prize cart successfully! Check the prize cart!")
            return redirect('frontEndUserProfile', username=username)
    except:
        messages.warning(request, "Can't be sent to prize cart! Contact with our customer support!")
        return redirect('frontEndUserProfile', username=username)

    return redirect('frontEndUserProfile', username=username)

@login_required(login_url='/fe/login/register')
def front_prize_cart_items(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # user prize items
    current_prize_cart_items = PrizeCart.objects.filter(user=request.user)

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user profile pic
    user_profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # user points wallet
    user_point_wallet = PointWallet.objects.filter(user=request.user).first()

    # user credit wallet
    user_credit_wallet = CreditWallet.objects.filter(user=request.user).first()

    # user winning chances
    user_winning_chances = WinningChance.objects.filter(user=request.user).first()

    # user orders
    order_list = OrderList.objects.filter(user=request.user).filter()

    # user default shipping address
    user_dflt_shipping_address = DefalutShippingInfo.objects.filter(user=request.user).first()

    # usr default billing address
    usr_default_biling_address = DefaultBillingInfo.objects.filter(user=request.user).first()

    # user prize list
    usr_won_prize_list = PrizeList.objects.filter(user=request.user)

    # all product category
    product_cat_list_all = ProductCategory.objects.all()

    # ads list on user profile
    user_profile_ads_list = UserProfileAds.objects.filter(status=True)

    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    context = {
        'current_prize_cart_items': current_prize_cart_items,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,

        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }

    return render(request, 'frontEnd/product_prize_delivery/prize_cart_items.html', context)


@login_required(login_url='/fe/login/register')
def front_prize_checkout(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # user default shipping address
    user_dflt_shipping_address = DefalutShippingInfo.objects.filter(user=request.user).first()

    # usr default billing address
    usr_default_biling_address = DefaultBillingInfo.objects.filter(user=request.user).first()


    # user cart status
    user_cart_status = Cart.objects.filter(user=request.user)

    # user wishlist status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    total_amount = 0
    if user_cart_status:
        for x in user_cart_status:
            if x.product.product_type == 'wsp':
                total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    # user current product prizes in the prize cart
    current_prize_cart_products = PrizeCart.objects.filter(user=request.user)

    context = {
        'current_prize_cart_products': current_prize_cart_products,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
        'total_amount': total_amount,
        'usr_deflt_shipping_addrss': user_dflt_shipping_address,
        'usr_deflt_billing_address': usr_default_biling_address,

        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }

    return render(request, 'frontEnd/product_prize_delivery/checkout.html', context)


@login_required(login_url='/fe/login/register')
def front_confirm_prize_delivery_order(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':

        # default shipping and billing address
        use_defalt_billing__adrs = request.POST.get('use_defalt_billin__adrs')
        use_defalt_shipping_addrss = request.POST.get('use_defalt_shipping_addrss')

        # billing informations
        country_b = request.POST.get('country_b')
        fname_b = request.POST.get('fname_b')
        lanme_b = request.POST.get('lanme_b')
        company_b = request.POST.get('company_b')
        address_b = request.POST.get('address_b')
        town_city_b = request.POST.get('town_city_b')
        state_b = request.POST.get('state_b')
        postcode_b = request.POST.get('postcode_b')
        email_b = request.POST.get('email_b')
        phone_b = request.POST.get('phone_b')

        # shipping info
        country_s = request.POST.get('country_s')
        fname_s = request.POST.get('fname_s')
        lanme_s = request.POST.get('lname_s')
        company_s = request.POST.get('company_s')
        address_s = request.POST.get('address_s')
        town_city_s = request.POST.get('town_city_s')
        state_s = request.POST.get('state_s')
        postcode_s = request.POST.get('postcode_s')
        email_s = request.POST.get('email_s')
        phone_s = request.POST.get('phone_s')

        order_note = request.POST.get('order_note')

        # random id generation for billing and shipping info
        id = uuid.uuid4()

        current_prize_cart_items = PrizeCart.objects.filter(Q(user=request.user) & Q(confirmed_for_delivery=False))

        if current_prize_cart_items:

            # save to "CurrentDelivryRequestPrizeProduct"
            for product in current_prize_cart_items:
                currnt_prize_delvery_request_item = CurrentDelivryRequestPrizeProduct.objects.create(
                    user=request.user,
                    product=product,
                    quantity=1,
                    is_current = True
                )

            product_prize_delivery_order = ProductPrizeDeliverOrder.objects.create(
                order_id=id,
                user=request.user,
                order_status='p',
                order_note=order_note,
            )
            for item in current_prize_cart_items:
                product_prize_delivery_order.items.add(item.product)
                product_prize_delivery_order.save()

            if use_defalt_billing__adrs:
                curnt_usr_billing_info = DefaultBillingInfo.objects.filter(user=request.user).first()

                if curnt_usr_billing_info:
                    billing_info_model = BillingInfo.objects.create(
                        info_id=id,
                        user=request.user,
                        use_defalut_address=True,
                        default_billingAddress=curnt_usr_billing_info,
                    )
                    product_prize_delivery_order.billing_info = billing_info_model
                    product_prize_delivery_order.save()
                else:
                    billing_info_model = BillingInfo.objects.create(
                        info_id=id,
                        user=request.user,
                        fname=fname_b,
                        lname=lanme_b,
                        country=country_b,
                        company=company_b,
                        address=address_b,
                        town_or_city=town_city_b,
                        state=state_b,
                        postcode=postcode_b,
                        email=email_b,
                        phone=phone_b
                    )
                    product_prize_delivery_order.billing_info = billing_info_model
                    product_prize_delivery_order.save()

            if use_defalt_shipping_addrss:
                curnt_usr_shipping_info = DefalutShippingInfo.objects.filter(user=request.user).first()
                if curnt_usr_shipping_info:
                    shipping_information_model = ShippingInfo.objects.create(
                        info_id=id,
                        user=request.user,
                        use_deflt_address=True,
                        default_shipping_address=curnt_usr_shipping_info,
                    )
                    product_prize_delivery_order.shipping_info = shipping_information_model
                    product_prize_delivery_order.save()
                else:
                    shipping_information_model = ShippingInfo.objects.create(
                        info_id=id,
                        user=request.user,
                        fname=fname_s,
                        lname=lanme_s,
                        country=country_s,
                        company=company_s,
                        address=address_s,
                        town_or_city=town_city_s,
                        state=state_s,
                        postcode=postcode_s,
                        email=email_s,
                        phone=phone_s,
                    )
                    product_prize_delivery_order.shipping_info = shipping_information_model
                    product_prize_delivery_order.save()
            messages.success(request, "Confirmed your delivery request!")
            return redirect('frontPrizeCheckout', username=request.user.username)
        else:
            return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontPrizeCheckout', username=request.user.username)

# user prize cart and delivery section ends*******************************************************

@login_required(login_url='/fe/login/register')
def front_ConvertPointInto_credit(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    # point wallet model
    pnt_wallet_model = PointWallet.objects.filter(user=request.user).first()

    if pnt_wallet_model:
        user_currnt_available_pnt = int(pnt_wallet_model.available)

        # assuming 100 pnts = 1 credit
        credit_amount = math.ceil((user_currnt_available_pnt) / 1000)

        # update user credit wallet
        user_credit_wallet = CreditWallet.objects.filter(user=request.user).first()

        if user_credit_wallet:
            user_credit_wallet.available = int(user_credit_wallet.available) + credit_amount
            user_credit_wallet.save()

            # updating point wallet after conversion
            pnt_wallet_model.available = 0
            pnt_wallet_model.save()

            messages.success(request, "Successfully converted!")
            return redirect('frontEndUserProfile', username=request.user.username)
        else:
            user_credit_wallet_model = CreditWallet.objects.create(user=request.user, available=credit_amount)

            # updating point wallet after conversion
            pnt_wallet_model.available = 0
            pnt_wallet_model.save()

            messages.success(request, "Successfully converted!")
            return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontEndUserProfile', username=request.user.username)

@login_required(login_url='/fe/login/register')
def front_send_email_invitation(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        mail_to = request.POST.get('email')
        msg = request.POST.get('msg')

        try:
            subject = "Invitation!"
            html_content = msg
            email = EmailMessage(subject, html_content, to=[mail_to])
            # email.content_subtype = 'html'
            email.send(fail_silently=False)

            # update user wallet
            user_wallet = PointWallet.objects.filter(user=request.user).first()
            if user_wallet:
                user_wallet.available = int(user_wallet.available) + 50
            else:
                user__wallet = PointWallet.objects.create(user=request.user, available=50)

            invitation_model = UserMailInvitations.objects.create(user=request.user, mail_to=mail_to, msg=msg)
            messages.success(request, "Invitation sent successfully! You got 50 reward points as bonus!")
            return redirect('frontEndUserProfile', username=request.user.username)
        except:
            messages.warning(request, "Invitation can't be sent! Try again!")
            return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontEndUserProfile', username=request.user.username)


@login_required(login_url='/fe/login/register')
def front_logoutUser(request):

    try:
        logout(request)
        return redirect('frontEndHome')
    except:
        pass
    return redirect('frontEndHome')


@login_required(login_url='/fe/login/register')
def front_updateProfile_picture(request):

    if request.method == 'POST':
        profile_picture = request.FILES['profile_picture']

        if profile_picture:
            fs = FileSystemStorage()
            try:
                # checking existing profile picture
                user_profile_pic = UserProfilePicture.objects.get(user=request.user)
                if user_profile_pic:
                    fs.delete(user_profile_pic.pic.name)
                user_profile_pic.pic = profile_picture
                user_profile_pic.save()
                messages.success(request, "Successfully update!")
                return redirect('frontEndUserProfile', username=request.user.username)
            except:
                user_profile_pic = UserProfilePicture(user=request.user, pic=profile_picture)
                user_profile_pic.save()
                messages.success(request, "Successfully update!")
                return redirect('frontEndUserProfile', username=request.user.username)

    return render(request, 'frontEnd/user_profile.html')

@login_required(login_url='/fe/login/register')
def front_update_username(reqeust):

    if reqeust.method == 'POST':
        current_username = reqeust.POST.get('current_username')
        new_username = reqeust.POST.get('new_username')

        if current_username and new_username:
            try:
                current_user = Account.objects.get(username=reqeust.user.username)
                user_with_crnt_username = Account.objects.filter(username=current_username).first()
                if current_user and user_with_crnt_username and current_user == user_with_crnt_username:
                    current_user.username = new_username
                    current_user.save()
                    messages.success(reqeust, "Successfully updated!")
                    logout(reqeust)
                    return redirect('frontEndLoginRegister')
            except:
                messages.warning(reqeust, "Wrong username! Try again!")
                return redirect('frontEndUserProfile', usernmae=reqeust.user.username)

    return render(reqeust, 'frontEnd/user_profile.html')

@login_required(login_url='/fe/login/register')
def front_update_internal_password(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')

        if email and username and old_pass:
            user = Account.objects.get(email=email)

            auth_user = authenticate(request, email=email, password=old_pass)

            if auth_user is not None:
                user.set_password(new_pass)
                user.save()
                messages.success(request, "Successfully updated!")
                return redirect('frontEndHome')
            else:
                messages.warning(request, "Can't be updated! Try again!")
                return redirect('frontEndUserProfile', username=request.user.username)

    return render(request, 'frontEnd/user_profile.html')

@login_required(login_url='/fe/login/register')
def front_add_default_billing_info(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        country_b = request.POST.get('country_b')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if DefaultBillingInfo.objects.filter(user=request.user).count() > 0:
            messages.warning(request, "Default address already exists!")
            return redirect('frontEndUserProfile', username=request.user.username)
        else:
            id = get_random_string(8)
            default_billing_adres = DefaultBillingInfo.objects.create(
                info_id=id,
                user=request.user,
                country=country_b,
                fname=name,
                address=address,
                town_or_city=city,
                postcode=postcode,
                email=email,
                phone=phone,
            )
            messages.success(request, "Deault billing address added successfully!")
            return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontEndUserProfile', username=request.user.username)

@login_required(login_url='/fe/login/register')
def front_update_default_billing_info(request, pk):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        country_b = request.POST.get('country_b')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')


        try:
            current_obj = get_object_or_404(DefaultBillingInfo, pk=pk)
            current_obj.country = country_b
            current_obj.fname = name
            current_obj.address = address
            current_obj.town_or_city = city
            current_obj.postcode = postcode
            current_obj.email = email
            current_obj.phone = phone
            current_obj.save()
            messages.success(request, "Billing information successfully updated!")
            return redirect('frontEndUserProfile', username=request.user.username)
        except:
            messages.warning(request, "Billing information not found!")
            return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontEndUserProfile', username=request.user.username)

@login_required(login_url='/fe/login/register')
def front_delete_default_billing_info(request, pk):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    try:
        current_obj = get_object_or_404(DefaultBillingInfo, pk=pk)
        current_obj.delete()
        messages.success(request, "Billing info successfully deleted!")
        return redirect('frontEndUserProfile', username=request.user.username)
    except:
        messages.warning(request, "Billing info can't be deleted!")
        return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontEndUserProfile', username=request.user.username)

@login_required(login_url='/fe/login/register')
def front_add_default_shipping_info(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        country_b = request.POST.get('country_b')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if DefalutShippingInfo.objects.filter(user=request.user).count() > 0:
            messages.warning(request, "Default shipping address already exists!")
            return redirect('frontEndUserProfile', username=request.user.username)
        else:
            id = get_random_string(8)

            default_shipping_adres = DefalutShippingInfo.objects.create(
                info_id=id,
                user=request.user,
                country=country_b,
                fname=name,
                address=address,
                town_or_city=city,
                postcode=postcode,
                email=email,
                phone=phone,
            )
            messages.success(request, "Default shipping address added successfully!")
            return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontEndUserProfile', username=request.user.username)

@login_required(login_url='/fe/login/register')
def front_update_default_shipping_info(request, pk):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        country_b = request.POST.get('country_b')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')


        try:
            current_obj = get_object_or_404(DefalutShippingInfo, pk=pk)
            current_obj.country = country_b
            current_obj.fname = name
            current_obj.address = address
            current_obj.town_or_city = city
            current_obj.postcode = postcode
            current_obj.email = email
            current_obj.phone = phone
            current_obj.save()
            messages.success(request, "Shipping information successfully updated!")
            return redirect('frontEndUserProfile', username=request.user.username)
        except:
            messages.warning(request, "Shipping information not found!")
            return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontEndUserProfile', username=request.user.username)

@login_required(login_url='/fe/login/register')
def front_delete_default_shipping_info(request, pk):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    try:
        current_obj = get_object_or_404(DefalutShippingInfo, pk=pk)
        current_obj.delete()
        messages.success(request, "Shipping info successfully deleted!")
        return redirect('frontEndUserProfile', username=request.user.username)
    except:
        messages.warning(request, "Shipping info can't be deleted!")
        return redirect('frontEndUserProfile', username=request.user.username)

    return redirect('frontEndUserProfile', username=request.user.username)

def front_refund_policy(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # current refund policy
    refund_policy = RefundPolicy.objects.filter().first()

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        total_amount = 0.0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,


            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'total_amount': total_amount,
            'refund_policy': refund_policy,
        }
        return render(request, 'frontEnd/policy/refund_policy.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,


        'refund_policy' : refund_policy,
    }
    return render(request, 'frontEnd/policy/refund_policy.html', context)


def front_return_policy(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # return policy
    return_policy = ReturnPolicy.objects.filter().first()

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        total_amount = 0.0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,


            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'total_amount': total_amount,
            'return_policy': return_policy,
        }
        return render(request, 'frontEnd/policy/return_policy.html', context)


    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,


        'return_policy': return_policy,
    }
    return render(request, 'frontEnd/policy/return_policy.html', context)


def front_security_policy(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # security policy
    security_policy = SecurityPolicy.objects.filter().first()

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        total_amount = 0.0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,


            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'total_amount': total_amount,
            'security_policy': security_policy,
        }
        return render(request, 'frontEnd/policy/security_policy.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'security_policy': security_policy,
    }

    return render(request, 'frontEnd/policy/security_policy.html', context)

def front_delivery_policy(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # delivery policy
    delivery_policy = DeliveryPolicy.objects.filter().first()

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        total_amount = 0.0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,


            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'total_amount': total_amount,
            'delivery_policy': delivery_policy,
        }
        return render(request, 'frontEnd/policy/delivery_policy.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'delivery_policy' : delivery_policy,
    }

    return render(request, 'frontEnd/policy/delivery_policy.html', context)

def front_about_us(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # delivery policy
    about_us = AboutUs.objects.filter().first()

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        total_amount = 0.0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,


            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'total_amount': total_amount,
            'about_us': about_us,
        }
        return render(request, 'frontEnd/company/about_us.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'about_us': about_us,
    }

    return render(request, 'frontEnd/company/about_us.html', context)

def front_cookie_policy(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # delivery policy
    cookie = CookiePolicy.objects.filter().first()

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        total_amount = 0.0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,


            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'total_amount': total_amount,
            'cookie': cookie,
        }
        return render(request, 'frontEnd/company/cookie.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'cookie': cookie,
    }

    return render(request, 'frontEnd/company/cookie.html', context)

def front_terms_conditions(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # delivery policy
    terms_condition = TermsConditions.objects.filter().first()

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        total_amount = 0.0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,


            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'total_amount': total_amount,
            'terms_condition': terms_condition,
        }
        return render(request, 'frontEnd/company/terms_condition.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,


        'terms_condition': terms_condition,
    }

    return render(request, 'frontEnd/company/terms_condition.html', context)

def front_privacy_policy(request):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    # privacy policy
    privacy_polilcy = PrivacyPolicy.objects.filter().first()

    if request.user.is_authenticated:
        # user cart status
        user_cart_status = Cart.objects.filter(user=request.user)

        # user wishlist status
        user_wishlist_status = WishList.objects.filter(user=request.user)

        total_amount = 0.0
        if user_cart_status:
            for x in user_cart_status:
                if x.product.product_type == 'wsp':
                    total_amount = round(total_amount + (float(x.product.price) * x.quantity), 2)
                if x.product.product_type == 'mcp':
                    total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)
        context = {
            'site_logo': site_logo,
            'contact_info': contact_info,
            'free_delivery_content_setting': free_delivery_content_setting,
            'safe_payment_content_setting': safe_payment_content_setting,
            'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
            'help_center_content_setting': help_center_content_setting,


            'user_cart_status': user_cart_status,
            'user_wishlist_status': user_wishlist_status,
            'total_amount': total_amount,
            'privacy_polilcy': privacy_polilcy,
        }
        return render(request, 'frontEnd/company/privacy.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'privacy_polilcy': privacy_polilcy,
    }

    return render(request, 'frontEnd/company/privacy.html', context)


# sign up for newletter/subscibe
def front_signup_for_newletter(request):

    if request.method == 'POST':

        email = request.POST.get('email')

        if email and SubscriberList.objects.filter(email=email).count() <= 0:
            subscriber_model = SubscriberList.objects.create(email=email)
            messages.success(request, "Thanks for signing up!")
            return redirect('frontEndHome')
        else:
            messages.warning(request, "You already signed up! But we appreciate your effort!")
            return redirect('frontEndHome')
    return redirect('frontEndHome')

def front_contact_us(request):

    site_logo = SiteLogo.objects.filter().first()

    contact_info = ContactUs.objects.first()
    # free delivery setting
    free_delivery_content_setting = FreeDelivery.objects.filter().first()

    # safe payment setting
    safe_payment_content_setting = SafePayment.objects.filter().first()

    # shopwith confidence setting
    shop_with_confidencce_content_setting = ShopWithConfidence.objects.filter().first()

    # help center setting
    help_center_content_setting = HelpCenter.objects.filter().first()

    if request.method == 'POST':
        name = request.POST.get('customerName')
        email = request.POST.get('customerEmail')
        subj = request.POST.get('contactSubject')
        msg = request.POST.get('contactMessage')

        if name and email and subj and msg:
            customer_msg_list = CustomerMessageList.objects.create(name=name, email=email, subj=subj, msg=msg)
            messages.success(request, "Thanks for contacting us. We will get back to you soon!")
            return redirect('frontContactUs')

        else:
            messages.warning(request, "Your message can't be proccesed! Try again!")
            return redirect('frontContactUs')

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }

    return render(request, 'frontEnd/contact_us.html', context)


# process user product prizes ***************************************************************


# process user product prizes ends***************************************************************




