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
from .models import PointWallet, WinningChance, PrizeList
from django.core.paginator import Paginator, EmptyPage



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


        'product_cat_list': product_cat_list,
        'product_list': products,

        'user_cart_status': user_cart_status,
        'user_wishlist_status': user_wishlist_status,
    }

    return render(request,  'frontEnd/index.html', context)

def front_home(request):

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

    product_cat_list = ProductCategory.objects.all()

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
    for x in product_cat_list:
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

    if product_cat_list:
        for cat in product_cat_list:
            current_cat_products = ProductList.objects.filter(Q(category=cat) | Q(cat_name__icontains=cat.name))[:6]
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
            'ip_exist': ip_exist,
            'main_banner_or_slider' : main_banner_or_slider,
            'product_cat_list': product_catList_with_prodct,
            'cats_in_subcats' : cats_in_subcats,
            'product_subcats' : product_subcats,
            'total_amount' : total_amount,
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
        return render(request, 'frontEnd/home.html', context)

    context = {
        'ip_exist': ip_exist,
        'main_banner_or_slider' : main_banner_or_slider,
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
    }

    return render(request, 'frontEnd/home.html', context)


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
        nid__card_no = request.POST['nid__card_no']
        user_role = request.POST['user_role']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if fname and lname and email and username and phone and nid__card_no and user_role and password and password == confirm_password:
            try:
                if len(Account.objects.filter(email=email)) <= 0 and len(Account.objects.filter(username=username)) <= 0 and len(Account.objects.filter(phone_no=phone)) <= 0:

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
                    verification_url = f'http://127.0.0.1:8000/user/account/veirfication/{username}/{phone}'
                    subject = f"Verification code"
                    html_content = render_to_string('backEnd_superAdmin/verification_template.html',
                                                    context={'verification_url': verification_url})
                    email = EmailMessage(subject, html_content, to=['nazmulhasan747406@gmail.com'])
                    email.content_subtype = 'html'
                    email.send(fail_silently=False)
                    # EmailThreading(email).start()


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
                    user.nid_no = nid__card_no
                    user.save()
                    messages.success(request, "Verification link sent to your mail!")
                    return redirect('frontEndLoginRegister')
            except:
                user = Account.objects.filter(email=email).first()
                if user:
                    user.delete()
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

    product_cat_list = ProductCategory.objects.all()

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
                'product_cat_list': product_cat_list,
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
            'product_cat_list': product_cat_list,
        }
        return render(request, 'frontEnd/search.html', context)

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,

        'product_cat_list': product_cat_list,
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

    product_cat_list = ProductCategory.objects.all()

    products = ProductList.objects.all()

    # product category list which has at least one product
    product_catList_with_prodct = []
    for x in product_cat_list:
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

    if product_cat_list:
        for cat in product_cat_list:
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
            if x.product.product_type == 'mcp':
                total_amount = round(total_amount + (x.product.new_price * x.quantity), 2)

    # user cart status
    user_wishlist_status = WishList.objects.filter(user=request.user)

    product_cart_list = Cart.objects.filter(user=request.user)

    context = {
        'current_user_usrname': username,
        'product_cart_list': product_cart_list,
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

    return render(request, 'frontEnd/checkout.html', context)

@login_required(login_url='/fe/login/register')
def front_confirm_order(request, username):

    if request.user.is_authenticated and request.user.is_buyer != True:
        return redirect('frontEndLoginRegister')


    if request.method == 'POST':
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
                    total_amount=total_amount,
                )
                for x in OrderedItem.objects.filter(Q(user=request.user) & Q(order_status='curnt')):
                    order_list_model.items.add(x)
                    x.order_status = 'curnt'
                    x.save()

                # removing cart items
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

    if request.user.is_authenticated:

        # getting current spinning chances
        current_chances = request.GET.get('current_chances')

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

        # grabing user won prize
        won_prize = request.GET.get('won_prize')

        if won_prize:
            user_prize_list_model = PrizeList(user=request.user, pirze=won_prize)
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

    # ajax part starts ***********************************************
    number_of_winnging_chance = request.GET.get('winning_chance_number')
    if request.is_ajax():
        return JsonResponse({'number_of_winnging_chance' : number_of_winnging_chance})


    if request.method == 'POST':
        number_of_winning_chance = request.POST.get('number_of_winning_chance')
        point_to_be_charged = request.POST.get('point_to_be_charged')

        if number_of_winning_chance and point_to_be_charged:
            user_point_wallet = PointWallet.objects.filter(user=request.user).first()

            if user_point_wallet and user_point_wallet.available:
                if int(user_point_wallet.available) >= int(point_to_be_charged):
                    if len(WinningChance.objects.filter(user=request.user)) > 0:
                        user_winning_chance_model = WinningChance.objects.get(user=request.user)
                        user_winning_chance_model.remaining_chances = number_of_winning_chance
                        user_winning_chance_model.save()

                        # updating point wallet after buying
                        user_point_wallet.available = int(user_point_wallet.available) - int(point_to_be_charged)
                        user_point_wallet.save()

                        messages.success(request, "Successfully bought new chances!")
                        return redirect('frontEndUserProfile', username=request.user.username)
                    else:
                        user_winning_chance_model = WinningChance(user=request.user,
                                                                  remaining_chances=number_of_winning_chance)
                        user_winning_chance_model.save()

                        # updating point wallet after buying
                        user_point_wallet.available = int(user_point_wallet.available) - int(point_to_be_charged)
                        user_point_wallet.save()

                        messages.success(request, "Successfully bought new chances!")
                        return redirect('frontEndUserProfile', username=request.user.username)
                else:
                    # current available chance
                    available__points = int(user_point_wallet.available)

                    # finding lack of points to buy chance
                    lack_of_points = int(point_to_be_charged) - available__points

                    # payable amount for buying chance for lack of points
                    payable_amount = (lack_of_points) / 20


                    context = {
                        'payable_amount' : payable_amount,
                        'available_points': available__points,
                        'necessary_points' : point_to_be_charged,
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
                payable_amount = int(point_to_be_charged) / 20

                context = {
                    'payable_amount': payable_amount,
                    'available_points': 0,
                    'necessary_points' : point_to_be_charged,
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

    # user payment status
    paid_amount = request.GET.get('paid_amount')
    purchased_chances = request.GET.get('purchased_chances')
    necessary_points = request.GET.get('necessary_points')

    # user winning chance model
    winning_chance_model = WinningChance.objects.filter(user=request.user).first()

    if winning_chance_model:
        winning_chance_model.remaining_chances = int(winning_chance_model.remaining_chances) + int(purchased_chances)
        winning_chance_model.save()
    if winning_chance_model is None:
        winning_chance_model = WinningChance.objects.create(user=request.user, remaining_chances=purchased_chances)

    # user point wallet
    point_wallet_model = PointWallet.objects.filter(user=request.user).first()

    if point_wallet_model:
        if point_wallet_model.spent:
            point_wallet_model.spent = float(point_wallet_model.spent) + (int(necessary_points) - (float(paid_amount) * 20))  # since $1 = 20 points
            point_wallet_model.save()
        if point_wallet_model.spent_amount:
            point_wallet_model.spent_amount = float(point_wallet_model.spent_amount) + float(paid_amount)
            point_wallet_model.save()

    if point_wallet_model is None:
        point_wallet = PointWallet(user=request.user, spent_amount=paid_amount)
        point_wallet.save()

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

    # user winning chances
    user_winning_chances = WinningChance.objects.filter(user=request.user).first()

    # user orders
    order_list = OrderList.objects.filter(user=request.user).filter()


    context = {
        'username' : username,
        'order_list' : order_list,
        'user_profile_pic' : user_profile_pic,
        'user_point_wallet' : user_point_wallet,
        'user_winning_chances' : user_winning_chances,
        'site_logo' : site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }
    return render(request, 'frontEnd/user_profile.html', context)

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
            email = EmailMessage(subject, html_content, to=['nazmulhasan747406@gmail.com'])
            email.content_subtype = 'html'
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







