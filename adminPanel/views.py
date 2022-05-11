import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import Account, VerificationCode, UserProfilePicture
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from verification.random_code_gen import rand_num_gen
from verification.email_threadings import EmailThreading
from django.utils import timezone
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from product.models import *
from game.models import *
import uuid
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
import json
import asyncio
import threading
from product.models import *
from advertisement.models import *


# woocomerce to connect with woocommerce store
from woocommerce import API
import asyncio



wcapi = API(
    url="https://www.ddmcustomz.ca",
    consumer_key="ck_d7b8e625408c67fc0351b88ea84e04b6f2657ce1",
    consumer_secret="cs_ba22b43fc833f3dc319f5385c027e6d79b73aaab",
    version="wc/v3",
    timeout=50,
)
# data = {
#     "payment_method": "bacs",
#     "payment_method_title": "Direct Bank Transfer",
#     "set_paid": True,
#     "billing": {
#         "first_name": "John",
#         "last_name": "Doe",
#         "address_1": "969 Market",
#         "address_2": "",
#         "city": "San Francisco",
#         "state": "CA",
#         "postcode": "94103",
#         "country": "US",
#         "email": "john.doe@example.com",
#         "phone": "(555) 555-5555",
#     },
#     "shipping": {
#         "first_name": "John",
#         "last_name": "Doe",
#         "address_1": "969 Market",
#         "address_2": "",
#         "city": "San Francisco",
#         "state": "CA",
#         "postcode": "94103",
#         "country": "US"
#     },
#     "line_items": [
#         {
#             "product_id": 93,
#             "quantity": 2
#         },
#         {
#             "product_id": 22,
#             "variation_id": 23,
#             "quantity": 1
#         }
#     ],
#     "shipping_lines": [
#         {
#             "method_id": "flat_rate",
#             "method_title": "Flat Rate",
#             "total": "10.00"
#         }
#     ]
# }

# def create_order(request):
#
#     order = wcapi.post("orders", data).json()
#     if order:
#         print(order)
#         return redirect('apHome')
#
#     return redirect('apHome')


# def add_woocommerce_product_to_product_list(obj, user):
#
#     if obj:
#         for x in obj:
#             if len(Product_list.objects.filter(woocmrce_product=x)) <= 0:
#                 product_list_model = Product_list(woocmrce_product=x, user=user)
#                 product_list_model.save()
#
#     return True

# ###################### woocommerce store section starts ***********************
@login_required(login_url='/ap/register/updated')
def ap_fetch_woocommerce_store_prdct(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # updated new section *****************************

    page = 1  # The first page number to loop is page 1
    try:
        while True:
            prods = wcapi.get('products', params={"per_page": 20, "page": page})
            page += 1
            if prods.text:
                p = json.loads(prods.text)

                try:
                    for x in p:
                        # combining multiple categories of one product
                        cats = ''
                        for cat in x['categories']:
                            cats = cats + cat['name'] + ' ,'

                        if len(ProductList.objects.filter(product_id=x['id'])) <= 0:
                            product_list_model = ProductList.objects.create(
                                user=request.user,
                                product_id=x['id'],
                                product_type='wsp',
                                title=x['name'],
                                slug=x['slug'],
                                details=x['description'],
                                regular_price=x['regular_price'],
                                price=x['price'],
                                total_sold=x['total_sales'],
                                in_stock=x['stock_status'],
                                avrg_rating=x['average_rating'],
                                rating_count=x['rating_count'],
                                cat_id=x['categories'][0]['id'],
                                cat_name=cats,
                                subcat_id='1',
                                subcat_name='subcat_name',
                                security_policy='apcp',
                                return_policy='apcp',
                                delivery_policy='apcp'
                            )

                            for img in x['images']:
                                product_img_model = ProductImg.objects.create(product_id=x['id'], product_type='wsp',
                                                                              img_link=img['src'])
                                product_list_model.productImg.add(product_img_model)
                                product_list_model.save()

                        if len(WoocommerceProductList.objects.filter(product_id=x['id'])) <= 0:

                            woocomrc_prdct_list_model = WoocommerceProductList.objects.create(
                                product_id=x['id'],
                                name=x['name'],
                                slug=x['slug'],
                                description=x['description'],
                                price=x['price'],
                                regular_price=x['regular_price'],
                                total_sales=x['total_sales'],
                                cat_id=x['categories'][0]['id'],
                                cat_name=x['categories'][0]['name'],
                                subcat_id='1',
                                subcat_name='subcat',
                                stock_status=x['stock_status'],
                                avrg_rating=x['average_rating'],
                                rating_count=x['rating_count']
                            )

                            for img in x['images']:
                                product_img_model = ProductImg.objects.create(product_id=x['id'], product_type='wsp',
                                                                              img_link=img['src'])

                                woocomrc_prdct_list_model.product_img.add(product_img_model)
                                woocomrc_prdct_list_model.save()
                except:

                    messages.warning(request, "Can't import products or server error! Try again!a")
                    return redirect('apWoocommerceStoreList')
            if len(json.loads(prods.text)) <= 0:
                break
    except:
        return redirect('apWoocommerceStoreList')

    # ends new section *********************************

    return redirect('apWoocommerceStoreList')
def ap_fetch_woocommerce_store_prdct(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # updated new section *****************************

    page = 1  # The first page number to loop is page 1
    try:
        while True:
            prods = wcapi.get('products', params={"per_page": 20, "page": page})
            page += 1
            if prods.text:
                p = json.loads(prods.text)

                try:
                    for x in p:
                        # combining multiple categories of one product
                        cats = ''
                        for cat in x['categories']:
                            cats = cats + cat['name'] + ' ,'

                        if len(ProductList.objects.filter(product_id=x['id'])) <= 0:
                            product_list_model = ProductList.objects.create(
                                user=request.user,
                                product_id=x['id'],
                                product_type='wsp',
                                title=x['name'],
                                slug=x['slug'],
                                details=x['description'],
                                regular_price=x['regular_price'],
                                price=x['price'],
                                total_sold=x['total_sales'],
                                in_stock=x['stock_status'],
                                avrg_rating=x['average_rating'],
                                rating_count=x['rating_count'],
                                cat_id=x['categories'][0]['id'],
                                cat_name=cats,
                                subcat_id='1',
                                subcat_name='subcat_name',
                                security_policy='apcp',
                                return_policy='apcp',
                                delivery_policy='apcp'
                            )

                            for img in x['images']:
                                product_img_model = ProductImg.objects.create(product_id=x['id'], product_type='wsp',
                                                                              img_link=img['src'])
                                product_list_model.productImg.add(product_img_model)
                                product_list_model.save()

                        if len(WoocommerceProductList.objects.filter(product_id=x['id'])) <= 0:

                            woocomrc_prdct_list_model = WoocommerceProductList.objects.create(
                                product_id=x['id'],
                                name=x['name'],
                                slug=x['slug'],
                                description=x['description'],
                                price=x['price'],
                                regular_price=x['regular_price'],
                                total_sales=x['total_sales'],
                                cat_id=x['categories'][0]['id'],
                                cat_name=x['categories'][0]['name'],
                                subcat_id='1',
                                subcat_name='subcat',
                                stock_status=x['stock_status'],
                                avrg_rating=x['average_rating'],
                                rating_count=x['rating_count']
                            )

                            for img in x['images']:
                                product_img_model = ProductImg.objects.create(product_id=x['id'], product_type='wsp',
                                                                              img_link=img['src'])

                                woocomrc_prdct_list_model.product_img.add(product_img_model)
                                woocomrc_prdct_list_model.save()
                except:

                    messages.warning(request, "Can't import products or server error! Try again!a")
                    return redirect('apWoocommerceStoreList')
            if len(json.loads(prods.text)) <= 0:
                break
    except:
        return redirect('apWoocommerceStoreList')

    # ends new section *********************************

    return redirect('apWoocommerceStoreList')


@login_required(login_url='/ap/register/updated')
def ap_wcmrce_prdct_details(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        # user profile picture
        profile_pic = UserProfilePicture.objects.filter(user=request.user).first()
        current_obj = WoocommerceProductList.objects.get(pk=pk)

        context = {
            'profile_pic' : profile_pic,
            'current_obj' : current_obj,
            'current_pk' : pk,
        }
        return render(request, 'backEnd_superAdmin/woocommerce_store/product_details.html', context)
    except:
        messages.warning(request, "Can't view the details! Try again!")
        return redirect('apWoocommerceStoreList')

    return render(request, 'backEnd_superAdmin/woocommerce_store/product_details.html')

@login_required(login_url='/ap/register/updated')
def ap_del_woocmmrce_prdct(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = WoocommerceProductList.objects.get(pk=pk)
        related_img_of_crnt_obj = ProductImg.objects.filter(product_id=current_obj.product_id)

        for obj in related_img_of_crnt_obj:
            obj.delete()
        current_obj.delete()
        messages.success(request, "Product has been deleted!")
        return redirect('apWoocommerceStoreList')
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('apWoocommerceStoreList')


    return redirect('apWoocommerceStoreList')

@login_required(login_url='/ap/register/updated')
def ap_woocommerce_store_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    woocomrce_product_list = WoocommerceProductList.objects.all()


    context = {
        'woocomrce_product_list' : woocomrce_product_list,
        'profile_pic' : profile_pic,
    }

    return render(request, "backEnd_superAdmin/woocommerce_store/woocommerce_store_prodct_list.html", context)

#*********************** Woocommerce section ends ***********************************************


# #######################order section ################################################
@login_required(login_url='/ap/register/updated')
def ap_current_orders(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    current_order_list = OrderList.objects.filter(Q(delivery_status=False) & Q(order_status='a') & Q(shipping_status=False))


    context = {
        'current_order_list' : current_order_list,
    }

    return render(request, 'backEnd_superAdmin/orders/current_order.html', context)

@login_required(login_url='/ap/register/updated')
def ap_current_order_details(request, order_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    current_order = OrderList.objects.get(order_id=order_id)


    context = {
        'current_order' : current_order,
    }

    return render(request, 'backEnd_superAdmin/orders/current_order_details.html', context)

@login_required(login_url='/ap/register/updated')
def ap_set_crrnt_order_to_on_the_way(request, order_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # current order
    try:
        current_order = OrderList.objects.filter(order_id=order_id).first()
        if current_order.order_status == 'a':
            current_order.shipping_status = True
            current_order.shipping_date = datetime.datetime.now()
            current_order.save()
            messages.success(request, 'Order status has been changed to "On The Way"!')
            return redirect('apCurrentOrderList')
        else:
            messages.warning(request, "Order is not approved yet!")
            return redirect('apCurrentOrderList')

    except:
        messages.warning(request, "Order status can't be changed! Try again!")
        return redirect('apCurrentOrderList')

    return redirect('apCurrentOrderList')


@login_required(login_url='/ap/register/updated')
def ap_cancel_order(request, order_id):


    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_order = OrderList.objects.filter(order_id=order_id).first()
        current_order.order_status = 'c'
        current_order.shipping_status = False
        current_order.delivery_status= False
        current_order.save()
        messages.success(request, 'Order has been cancelled!')
        return redirect('apCurrentOrderList')
    except:
        messages.success(request, "Order status can't be cancelled! Try again!")
        return redirect('apCurrentOrderList')

    return redirect('apCurrentOrderList')


# on the way ******************
@login_required(login_url='/ap/register/updated')
def ap_on_the_way_order_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # order list which already shipped for delivery

    order_list = OrderList.objects.filter(Q(order_status='a') & Q(delivery_status=False) & Q(shipping_status=True))


    context = {
        'order_list' : order_list,
    }

    return render(request, 'backEnd_superAdmin/orders/on_the_way.html', context)

@login_required(login_url='/ap/register/updated')
def ap_set_to_delivered(request, order_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_order = OrderList.objects.filter(order_id=order_id).first()
        if current_order.order_status == 'a' and current_order.delivery_status == False and current_order.shipping_status == True:
            current_order.delivery_status = True
            current_order.delivery_date = datetime.datetime.now()
            current_order.save()
            messages.success(request, "Order status has been changed to 'Delivered' !")
            return redirect('apOnTheWayOrderList')
        else:
            messages.warning(request, "Order status can't be changed! Check 'Order Status/Delivery Status/Shipping Status'!")
            return redirect('apOnTheWayOrderList')
    except:
        messages.warning(request,"Order not found! Try again!")
        return redirect('apOnTheWayOrderList')

    return redirect('apOnTheWayOrderList')


@login_required(login_url='/ap/register/updated')
def ap_delivered_order_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    order_list = OrderList.objects.filter(Q(delivery_status=True) & Q(shipping_status=True) & Q(order_status='a'))

    context = {
        'delivered_ordered_list' : order_list,
    }

    return render(request, 'backEnd_superAdmin/orders/delivered.html', context)


@login_required(login_url='/ap/register/updated')
def ap_cancelled_order_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    cancelled_order_list = OrderList.objects.filter(order_status='c')

    context = {
        'cancelled_order_list': cancelled_order_list,
    }

    return render(request, 'backEnd_superAdmin/orders/cancelled.html', context)

# *********************************** ends order section *********************************************

# user profile setting section *****************************************************************
@login_required(login_url='/ap/register/updated')
def ap_update_user_profile_picture(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        profile_picture = request.FILES['profile_pic']

        if profile_picture:
            fs = FileSystemStorage()
            try:
                # checking existing profile picture
                user_profile_pic = UserProfilePicture.objects.get(user=request.user)
                if user_profile_pic:
                    fs.delete(user_profile_pic.pic.name)
                user_profile_pic.pic = profile_picture
                user_profile_pic.save()
                messages.success(request, "Successfully updated!")
                return redirect('apMyProfile', username=request.user.username)
            except:
                user_profile_pic = UserProfilePicture(user=request.user, pic=profile_picture)
                user_profile_pic.save()
                messages.success(request, "Successfully updated!")
                return redirect('apMyProfile', username=request.user.username)

    return render(request, 'backEnd_superAdmin/profile/my-profile.html', context)


@login_required(login_url='/ap/register/updated')
def ap_update_user_full_name(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        if fname and lname:
            try:
                user = Account.objects.get(email=request.user.email)
                user.fname = fname
                user.laname = lname
                user.save()
                messages.success(request, "Successfully updated!")
                return redirect('apMyProfile', username=request.user.username)
            except:
                messages.warning(request, "Can't be updated!")
                return redirect('apMyProfile', username=request.user.username)

    return render(request, 'backEnd_superAdmin/profile/my-profile.html')

@login_required(login_url='/ap/register/updated')
def ap_update_user_password(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')

        if email and username and old_pass:
            try:
                user = Account.objects.get(email=email)
                auth_user = authenticate(request, email=email, password=old_pass)

                if auth_user is not None:
                    user.set_password(new_pass)
                    user.save()
                    messages.success(request, "Successfully updated!")
                    return redirect("apSuperAdminRegister")
            except:
                messages.warning(request, "Can't be updated! Try again!")
                return redirect('apMyProfile', username=request.user.username)

    return render(request, 'backEnd_superAdmin/profile/my-profile.html')

# user profile setting section ends*****************************************************************

def ap_RegisterSuperUser(request):


    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmpass = request.POST['con_pass']


        if name and email and username and phone and password and confirmpass:
            if  len(Account.objects.filter(email=email)) <= 0 and len(Account.objects.filter(username=username)) <= 0 and len(Account.objects.filter(phone_no=phone)) <= 0:
                if password == confirmpass:
                    try:
                        user_account = Account.objects.create_superuser(email=email, username=username, phone_no=phone, password=password)
                        user_account.fname = name
                        user_account.status = '0'
                        user_account.is_active = False
                        user_account.save()

                        # # sending verification email with code*********************************
                        # verification__code = rand_num_gen(3)
                        #
                        # # save to verification code model by user
                        # verification_code_model = VerificationCode(user_email=email, code=verification__code)
                        # verification_code_model.save()

                        # request.session.flush()
                        # request.session['v_email'] = email
                        # request.session['v_code'] = verification__code
                        # request.session.set_expiry(300)

                        subject = f"Verification Link"
                        verification_url = f"Click to verify account: http://127.0.0.1:8000/user/account/veirfication/{username}/{phone}/"
                        html_content = render_to_string('backEnd_superAdmin/verification_template.html',
                                                        context={'verification_url': verification_url})
                        email = EmailMessage(subject, html_content, to=[email])
                        email.content_subtype = 'html'
                        EmailThreading(email).start()
                        messages.success(request, "Verification link sent to your email!")
                        return redirect('apSuperAdminRegister')
                    except:
                        messages.warning(request, "Can't create account! Try again!")
                        return redirect('apSuperAdminRegister')
                    # ends sending verification email with code*************************

                else:
                    messages.warning(request, "Password didn't match! Try again!")
                    return redirect('apSuperAdminRegister')

    return render(request, 'backEnd_superAdmin/register.html')

def ap_loginSuperUser(request):

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if email and username and password:
            try:
                user = Account.objects.get(email=email)
                try:
                    if user.status == '1' and user.is_active == True:
                        authenticate_user = authenticate(request, email=email, password=password)
                        if authenticate_user is not None:
                            login(request, authenticate_user)
                            return redirect('apHome')
                        else:
                            messages.warning(request, "You are not authenticated yet!")
                            return redirect('apSuperAdminRegister')
                    else:
                        messages.warning(request, "Please verify your account to acccess!")
                        return redirect('apSuperAdminRegister')
                except:
                    messages.warning(request, "User not found!")
                    return redirect('apSuperAdminRegister')
            except:
                messages.warning(request, 'Wrong username or email')
                return redirect('apSuperAdminRegister')

    return render(request, 'backEnd_superAdmin/log_in.html')


@login_required(login_url='/ap/register/updated')
def logoutSuperUser(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        logout(request)
        return redirect('apSuperAdminRegister')
    except:
        pass
    redirect('apSuperAdminRegister')


@login_required(login_url='/ap/register/updated')
def index(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    context = {
        'profile_pic': profile_pic
    }

    return render(request, 'backEnd_superAdmin/index.html', context)

@login_required(login_url='/ap/register/updated')
def home(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    user_list = Account.objects.all()

    # total orders
    total_number_of_orders = OrderList.objects.all().count()

    # total number of registered user
    total_registered_usr = Account.objects.all().count()

    # total number of products
    total_number_of_products = ProductList.objects.all().count()

    context = {
        'user_list' : user_list,
        'profile_pic' : profile_pic,
        'total_number_of_orders': total_number_of_orders,
        'total_registered_usr': total_registered_usr,
        'total_number_of_products': total_number_of_products,
    }

    return render(request, 'backEnd_superAdmin/home.html', context)

@login_required(login_url='/ap/register/updated')
def deactivateUser(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_user = Account.objects.get(pk=pk)
        current_user.is_active = False
        current_user.save()
        messages.success(request, "User account has been deactivated!")
        return redirect('apHome')
    except:
        messages.warning(request, "Sorry! User not found!")
        return redirect('apHome')
    return redirect('apHome')

@login_required(login_url='/ap/register/updated')
def activateUser(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_user = Account.objects.get(pk=pk)
        current_user.is_active = True
        current_user.save()
        messages.success(request, "User account has been activated!")
        return redirect('apHome')
    except:
        messages.warning(request, "Sorry! User not found!")
        return redirect('apHome')
    return redirect('apHome')

@login_required(login_url='/ap/register/updated')
def removeUser(request, pk):


    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_user = Account.objects.get(pk=pk)
        current_user.delete()
        messages.success(request, "User account has been removed!")
        return redirect('apHome')
    except:
        messages.warning(request, "Sorry! User not found!")
        return redirect('apHome')
    return redirect('apHome')


@login_required(login_url='/ap/register/updated')
def ap_add_product_category(request):


    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        name = request.POST['cat__name']

        if name and len(ProductCategory.objects.filter(name=name)) <= 0:
            product_cat_model = ProductCategory(name=name)
            product_cat_model.save()
            messages.success(request, 'Successfully added!')
            return redirect('apAddProductCategory')
        else:
            messages.success(request, 'Category name already exists!')
            return redirect('apAddProductCategory')

    # product category list
    product_cats_list = ProductCategory.objects.all()

    context = {
        'product_cats_list' : product_cats_list,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product_cat/add_product_category.html', context)


# product cateory section*******************************************************

@login_required(login_url='/ap/register/updated')
def ap_edit_product_category(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        name = request.POST['name']
        if name and len(ProductCategory.objects.filter(name=name)) <= 0:
            product_cat_model = ProductCategory.objects.get(pk=pk)
            product_cat_model.name = name
            product_cat_model.save()
            messages.success(request, 'Successfully updated!')
            return redirect('apAddProductCategory')
        else:
            messages.success(request, 'Category name already exists!')
            return redirect('apAddProductCategory')

    return redirect('apAddProductCategory')

@login_required(login_url='/ap/register/updated')
def ap_del_product_category(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        category = ProductCategory.objects.get(pk=pk)
        category.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddProductCategory')
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('apAddProductCategory')

    return redirect('apAddProductCategory')


# product sub-category section*******************************************************
@login_required(login_url='/ap/register/updated')
def ap_add_product_subcat(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        name = request.POST['subcat__name']
        if name and len(ProductSubCategory.objects.filter(name=name)) <= 0:

            product_cat_model = ProductCategory.objects.get(pk=pk)
            product_subcat_model = ProductSubCategory(category=product_cat_model, name=name)
            product_subcat_model.save()

            messages.success(request, 'Successfully added!')
            return redirect('apAddSubcategory', pk=pk)
        else:
            messages.warning(request, 'Category name already exists!')
            return redirect('apAddSubcategory', pk=pk)

    # product sub-category list
    product_subcat_list = ProductSubCategory.objects.filter(category=pk)

    context = {
        'cat_pk': pk,
        'product_subcat_list' : product_subcat_list,
        'profile_pic' : profile_pic,
    }
    return render(request, 'backEnd_superAdmin/product_cat/product_subcategory.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_product_subcat(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    current_obj = ProductSubCategory.objects.get(pk=pk)

    try:
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddSubcategory', pk=current_obj.category.pk)
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('apAddSubcategory', pk=current_obj.category.pk)

    return redirect('apAddSubcategory', pk=current_obj.category.pk)

# add custom product section updated************************************************
@login_required(login_url='/ap/register/updated')
def ap_all_products(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # product list
    product_list = ProductList.objects.all()

    context = {
        'product_list' : product_list,
    }

    return render(request, 'backEnd_superAdmin/product/all_products.html', context)

@login_required(login_url='/ap/register/updated')
def ap_add_admin_custsom_product(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    product_cat = ProductCategory.objects.all()
    product_subcat = ProductSubCategory.objects.all()

    if request.method == 'GET':
        # getting current product category ajax request
        current_product_cat = request.GET.get('current_prodct_cat')

        # product subcategory by selected category
        subcat_of_current_cat = list(ProductSubCategory.objects.filter(category=current_product_cat).values())

        if request.is_ajax():
            return JsonResponse({'crrnt_product_subcat': subcat_of_current_cat})

    if request.method == 'POST':
        title = request.POST['title']
        brand__name = request.POST['brand__name']
        category = request.POST['category']
        sub_category = request.POST.get('sub_category')
        short_des = request.POST['short_des']
        details = request.POST['details']
        new_price = float(request.POST['new_price'])
        old_price = float(request.POST['old_price'])
        use_cases = request.POST['use_cases']
        benefits = request.POST['benefits']
        thumbnail_img = request.FILES['product__main__thumbnail__img']
        store_link = request.POST['store_link']
        store__name = request.POST['store__name']
        about_store = request.POST['about_store']
        in_stock = request.POST['in_stock']
        policy = request.POST['policy']
        security_policy = request.POST['security_policy']
        return_policy = request.POST['return_policy']
        delivery_policy = request.POST['delivery_policy']

        sponsor_status = request.POST.get('sponsor__status')

        product_id = uuid.uuid4()

        curnt_product_cat = ProductCategory.objects.filter(pk=category).first()

        curnt_product_subcat = None

        if sub_category:
            curnt_product_subcat = ProductSubCategory.objects.filter(pk=sub_category).first()


        try:
            extra_imgs = request.FILES.getlist('product__extra__images')
            length_of_extra_imgs = len(extra_imgs)

            if length_of_extra_imgs >= 0:
                for img in extra_imgs:
                    product_img_model = ProductImg.objects.create(product_id=product_id, product_type='mcp', img=img)

                if policy == 'company':
                    product_list_model = ProductList.objects.create(
                        product_id=product_id,
                        product_type='mcp',
                        user=request.user,
                        category=curnt_product_cat,
                        subcategory=curnt_product_subcat,
                        title=title,
                        brand_name=brand__name,
                        old_price=float(old_price),
                        new_price=float(new_price),
                        short_des=short_des,
                        details=details,
                        product_thumbnail=thumbnail_img,
                        use_case=use_cases,
                        benefits=benefits,
                        security_policy='apcp',
                        return_policy='apcp',
                        delivery_policy='apcp',
                        store_name=store__name,
                        store_link=store_link,
                        about_store=about_store,
                        in_stock=in_stock,
                        policy_followed=policy,
                        sponsor_status=sponsor_status
                    )
                    product_extra_img_list = ProductImg.objects.filter(product_id=product_id)
                    if product_extra_img_list:
                        for img in product_extra_img_list:
                            product_list_model.productImg.add(img)
                            product_list_model.save()

                if policy == 'own':
                    product_list_model = ProductList.objects.create(
                        product_id=product_id,
                        product_type='mcp',
                        user=request.user,
                        category=curnt_product_cat,
                        subcategory=curnt_product_subcat,
                        title=title,
                        brand_name=brand__name,
                        old_price=old_price,
                        new_price=new_price,
                        short_des=short_des,
                        details=details,
                        product_thumbnail=thumbnail_img,
                        use_case=use_cases,
                        benefits=benefits,
                        security_policy=security_policy,
                        return_policy=return_policy,
                        delivery_policy=delivery_policy,
                        store_name=store__name,
                        store_link=store_link,
                        about_store=about_store,
                        in_stock=in_stock,
                        policy_followed=policy,
                    )
                    product_extra_img_list = ProductImg.objects.filter(product_id=product_id)
                    if product_extra_img_list:
                        for img in product_extra_img_list:
                            product_list_model.productImg.add(img)
                            product_list_model.save()

                # saving to Game sponsored product list
                if sponsor_status == 'yes':
                    spnsored_prdct = ProductList.objects.get(product_id=product_id)
                    sponsord_prdct_for_game = SponsoredProductForPrize(product=spnsored_prdct)
                    sponsord_prdct_for_game.save()

                messages.success(request, "Successfully added!")
                return redirect('apAddAdminCustomProduct')

        except:
            if policy == 'company':
                product_list_model = ProductList.objects.create(
                    product_id=product_id,
                    product_type='mcp',
                    user=request.user,
                    category=curnt_product_cat,
                    subcategory=curnt_product_subcat,
                    title=title,
                    brand_name=brand__name,
                    old_price=float(old_price),
                    new_price=float(new_price),
                    short_des=short_des,
                    details=details,
                    product_thumbnail=thumbnail_img,
                    use_case=use_cases,
                    benefits=benefits,
                    security_policy='apcp', # apcp== As per company policy
                    return_policy='apcp',  # apcp== As per company policy
                    delivery_policy='apcp', # apcp== As per company policy
                    store_name=store__name,
                    store_link=store_link,
                    about_store=about_store,
                    in_stock=in_stock,
                    policy_followed=policy,
                    sponsor_status=sponsor_status
                )
                product_extra_img_list = ProductImg.objects.filter(product_id=product_id)
                if product_extra_img_list:
                    for img in product_extra_img_list:
                        product_list_model.productImg.add(img)
                        product_list_model.save()

            if policy == 'own':
                product_list_model = ProductList.objects.create(
                    product_id=product_id,
                    product_type='mcp',
                    user=request.user,
                    category=curnt_product_cat,
                    subcategory=curnt_product_subcat,
                    title=title,
                    brand_name=brand__name,
                    old_price=old_price,
                    new_price=new_price,
                    short_des=short_des,
                    details=details,
                    product_thumbnail=thumbnail_img,
                    use_case=use_cases,
                    benefits=benefits,
                    security_policy=security_policy,
                    return_policy=return_policy,
                    delivery_policy=delivery_policy,
                    store_name=store__name,
                    store_link=store_link,
                    about_store=about_store,
                    in_stock=in_stock,
                    policy_followed=policy,
                )
                product_extra_img_list = ProductImg.objects.filter(product_id=product_id)
                if product_extra_img_list:
                    for img in product_extra_img_list:
                        product_list_model.productImg.add(img)
                        product_list_model.save()

            # saving to Game sponsored product list
            if sponsor_status == 'yes':
                spnsored_prdct = ProductList.objects.get(product_id=product_id)
                sponsord_prdct_for_game = SponsoredProductForPrize(product=spnsored_prdct)
                sponsord_prdct_for_game.save()

            messages.success(request, "Successfully added!")
            return redirect('apAddAdminCustomProduct')

    context = {
        'product_cat' : product_cat,
        'product_subcat' : product_subcat,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/add__product.html', context)


@login_required(login_url='/ap/register/updated')
def ap_admin_custom_product_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # product list
    product_list = ProductList.objects.filter(Q(user=request.user) & Q(product_type='mcp'))

    context = {
        'product_list' : product_list,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/product_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_admin_custom_product_details(request, pk, product_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # current obj
    current_product = ProductList.objects.get(pk=pk)

    context = {
        'current_pk' : pk,
        'current_prodct_id' : product_id,
        'current_product': current_product,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/product_details.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_admin_custom_product(request, pk, product_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # product category
    product_category = ProductCategory.objects.all()

    # product sub-cat
    product_subcat = ProductSubCategory.objects.all()


    # get current obj
    current_product_data = ProductList.objects.get(pk=pk)

    # current product's extra image obj
    # currnt_product_extra_img = ProductImg.objects.filter(product=current_product_data).first()

    if request.method == 'POST':
        title = request.POST['title']
        brand__name = request.POST['brand__name']
        category = request.POST['category']
        sub_category = request.POST.get('sub_category')
        short_des = request.POST['short_des']
        details = request.POST['details']
        new_price = float(request.POST['new_price'])
        old_price = float(request.POST['old_price'])
        use_cases = request.POST['use_cases']
        benefits = request.POST['benefits']
        store_link = request.POST['store_link']
        store__name = request.POST['store__name']
        about_store = request.POST['about_store']
        in_stock = request.POST['in_stock']
        policy = request.POST['policy']
        security_policy = request.POST['security_policy']
        return_policy = request.POST['return_policy']
        delivery_policy = request.POST['delivery_policy']
        sponsor_status = request.POST.get('sponsor__status')

        delete_old_images = request.POST.get('delete_old_images')

        curnt_product_cat = ProductCategory.objects.filter(pk=category).first()

        curnt_product_subcat = None
        if sub_category:
            curnt_product_subcat = ProductSubCategory.objects.filter(pk=sub_category).first()

        fs = FileSystemStorage()

        try:

            if delete_old_images == 'on':
                # grabing extra images of current object
                currnt_obj_extra_img_list = ProductImg.objects.filter(product_id=current_product_data.product_id)

                if currnt_obj_extra_img_list:
                    for img in currnt_obj_extra_img_list:
                        fs.delete(img.img.name)
                        img.delete()

            thumbnail_img = request.FILES['product__main__thumbnail__img']

            # removing/saving product from sponsored product prize list if sponsored status is false
            if sponsor_status == 'no' and len(SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                sponsored_product.delete()
            if sponsor_status == 'yes' and len(SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                sponsored_product = SponsoredProductForPrize(product=current_product_data)
                sponsored_product.save()

            # deleting current thumbnail
            if thumbnail_img:
                fs.delete(current_product_data.product_thumbnail.name)

                extra_imgs = request.FILES.getlist('product__extra__images')
                length_of_extra_imgs = len(extra_imgs)
                if length_of_extra_imgs > 0:
                    for img in extra_imgs:
                        product_extra_img_model = ProductImg.objects.create(product_id=current_product_data.product_id, product_type='mcp', img=img)
                        current_product_data.productImg.add(product_extra_img_model)
                        current_product_data.save()

                    if policy == 'company':
                        current_product_data.category = curnt_product_cat
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.old_price = float(old_price)
                        current_product_data.new_price = float(new_price)
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = 'apcp' # apcp== As per company policy
                        current_product_data.return_policy = 'apcp'
                        current_product_data.delivery_policy = 'apcp'
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()

                    if policy == 'own':
                        current_product_data.category = curnt_product_cat
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.old_price = float(old_price)
                        current_product_data.new_price = float(new_price)
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()

                    messages.success(request, "Successfully updated!")
                    return redirect('apAdminCustomProductList')

                else:
                    if policy == 'company':
                        current_product_data.category = curnt_product_cat
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.old_price = float(old_price)
                        current_product_data.new_price = float(new_price)
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = 'apcp' # apcp == As per company policy
                        current_product_data.return_policy = 'apcp'
                        current_product_data.delivery_policy = 'apcp'
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == 'own':
                        current_product_data.category = curnt_product_cat
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.title = title
                        current_product_data.brand_name = brand__name
                        current_product_data.old_price = float(old_price)
                        current_product_data.new_price = float(new_price)
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    messages.success(request, "Successfully updated!")
                    return redirect('apAdminCustomProductList')
        except:

            if delete_old_images == 'on':
                # grabing extra images of current object
                currnt_obj_extra_img_list = ProductImg.objects.filter(product_id=current_product_data.product_id)

                if currnt_obj_extra_img_list:
                    for img in currnt_obj_extra_img_list:
                        fs.delete(img.img.name)
                        img.delete()

            extra_imgs = request.FILES.getlist('product__extra__images')

            # removing/saving product from sponsored product prize list if sponsored status is false
            if sponsor_status == 'no' and len(SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                sponsored_product.delete()

            if sponsor_status == 'yes' and len(SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                sponsored_product = SponsoredProductForPrize(product=current_product_data)
                sponsored_product.save()

            length_of_extra_imgs = len(extra_imgs)
            if length_of_extra_imgs > 0:

                for img in extra_imgs:
                    product_extra_img_model = ProductImg.objects.create(product_id=current_product_data.product_id,
                                                                        product_type='mcp', img=img)
                    current_product_data.productImg.add(product_extra_img_model)
                    current_product_data.save()

                if policy == 'company':
                    current_product_data.category = curnt_product_cat
                    current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.old_price = float(old_price)
                    current_product_data.new_price = float(new_price)
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = 'apcp'
                    current_product_data.return_policy = 'apcp'
                    current_product_data.delivery_policy = 'apcp'
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == 'own':
                    current_product_data.category = curnt_product_cat
                    current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.old_price = float(old_price)
                    current_product_data.new_price = float(new_price)
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                messages.success(request, "Successfully updated!")
                return redirect('apAdminCustomProductList')
            else:
                if policy == 'company':
                    current_product_data.category = curnt_product_cat
                    current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.old_price = float(old_price)
                    current_product_data.new_price = float(new_price)
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = 'apcp'
                    current_product_data.return_policy = 'apcp'
                    current_product_data.delivery_policy = 'apcp'
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == 'own':
                    current_product_data.category = curnt_product_cat
                    current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.old_price = float(old_price)
                    current_product_data.new_price = float(new_price)
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                messages.success(request, "Successfully updated!")
                return redirect('apAdminCustomProductList')


    context = {
        'current_pk' : pk,
        'current_product_id' : product_id,
        'current_product_data' : current_product_data,
        'product_category' : product_category,
        'product_subcategory' : product_subcat,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/update_product.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_admin_custom_product(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = ProductList.objects.get(pk=pk)

        fs = FileSystemStorage()
        # checking wheathe it has any extra images or not
        related_imgs_of_currnt_obj = ProductImg.objects.filter(product_id=current_obj.product_id)
        if related_imgs_of_currnt_obj:
            for img in related_imgs_of_currnt_obj:
                fs.delete(img.img.name)
                img.delete()


        # deleting product thumbnail obj
        fs.delete(current_obj.product_thumbnail.name)
        current_obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAdminCustomProductList')
        redirect('apAdminCustomProductList')
    except:
        messages.warning(request, 'Can not be deleted! Try again!')
        return redirect('apAdminCustomProductList')
        redirect('apAdminCustomProductList')

    return redirect('apAdminCustomProductList')

@login_required(login_url='/ap/register/updated')
def ap__update_admin_wcmrce_product(request, pk, product_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    # product category
    product_category = ProductCategory.objects.all()

    # product sub-cat
    product_subcat = ProductSubCategory.objects.all()


    # get current obj
    current_product_data = ProductList.objects.get(pk=pk)


    if request.method == 'POST':
        title = request.POST['title']
        brand__name = request.POST['brand__name']
        category = request.POST['category']
        sub_category = request.POST['sub_category']
        short_des = request.POST['short_des']
        details = request.POST['details']
        new_price = request.POST['new_price']
        old_price = request.POST['old_price']
        use_cases = request.POST['use_cases']
        benefits = request.POST['benefits']
        store_link = request.POST['store_link']
        store__name = request.POST['store__name']
        about_store = request.POST['about_store']
        in_stock = request.POST['in_stock']
        policy = request.POST['policy']
        security_policy = request.POST['security_policy']
        return_policy = request.POST['return_policy']
        delivery_policy = request.POST['delivery_policy']
        sponsor_status = request.POST.get('sponsor__status')

        delete_old_images = request.POST.get('delete_old_images')

        curnt_product_cat = None
        curnt_product_subcat = None

        if category:
            curnt_product_cat = ProductCategory.objects.filter(pk=category).first()
        if sub_category:
            curnt_product_subcat = ProductSubCategory.objects.filter(pk=sub_category).first()

        fs = FileSystemStorage()

        if delete_old_images:
            related_img_model = ProductImg.objects.filter(product_id=current_product_data.product_id)

            if related_img_model:
                for img in related_img_model:
                    if img.img:
                        fs.delete(img.img.name)
                        img.delete()

        try:
            thumbnail_img = request.FILES['product__main__thumbnail__img']

            # removing/saving product from sponsored product prize list if sponsored status is false
            if sponsor_status == 'no' and len(
                    SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                sponsored_product.delete()
            if sponsor_status == 'yes' and len(
                    SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                sponsored_product = SponsoredProductForPrize(product=current_product_data)
                sponsored_product.save()

            # deleting current thumbnail
            if thumbnail_img:
                if current_product_data.product_thumbnail:
                    fs.delete(current_product_data.product_thumbnail.name)

                extra_imgs = request.FILES.getlist('product__extra__images')
                length_of_extra_imgs = len(extra_imgs)

                if length_of_extra_imgs > 0:

                    for img in extra_imgs:
                        related_img_model = ProductImg.objects.create(product_id=current_product_data.product_id, img=img)
                        current_product_data.productImg.add(related_img_model)
                        current_product_data.save()

                    if policy == 'company':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                            current_product_data.save()
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                            current_product_data.save()

                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = "apcp" # apcp == as per company policy
                        current_product_data.return_policy = "apcp"
                        current_product_data.delivery_policy = "apcp"
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == 'own':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                            current_product_data.save()
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                            current_product_data.save()
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == '':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                            current_product_data.save()
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                            current_product_data.save()
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()

                    # check if there is any extra images exists for current product

                    messages.success(request, "Successfully updated!")
                    return redirect('apAllProductList')

                else:
                    if policy == 'company':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat

                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = "apcp"
                        current_product_data.return_policy = "apcp"
                        current_product_data.delivery_policy = "apcp"
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == 'own':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.title = title
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()
                    if policy == '':
                        if curnt_product_cat:
                            current_product_data.category = curnt_product_cat
                            current_product_data.save()
                        if curnt_product_subcat:
                            current_product_data.subcategory = curnt_product_subcat
                            current_product_data.save()
                        current_product_data.title = title
                        current_product_data.product_thumbnail = thumbnail_img
                        current_product_data.brand_name = brand__name
                        current_product_data.regular_price = old_price
                        current_product_data.price = new_price
                        current_product_data.short_des = short_des
                        current_product_data.details = details
                        current_product_data.use_case = use_cases
                        current_product_data.benefits = benefits
                        current_product_data.security_policy = security_policy
                        current_product_data.return_policy = return_policy
                        current_product_data.delivery_policy = delivery_policy
                        current_product_data.store_name = store__name
                        current_product_data.store_link = store_link
                        current_product_data.about_store = about_store
                        current_product_data.in_stock = in_stock
                        current_product_data.policy_followed = policy
                        current_product_data.sponsor_status = sponsor_status
                        current_product_data.save()

                    messages.success(request, "Successfully updated!")
                    return redirect('apAllProductList')
        except:

            extra_imgs = request.FILES.getlist('product__extra__images')

            if extra_imgs:

                for img in extra_imgs:
                    related_img_model = ProductImg.objects.create(product_id=current_product_data.product_id, img=img)
                    current_product_data.productImg.add(related_img_model)
                    current_product_data.save()

                # removing/saving product from sponsored product prize list if sponsored status is false
                if sponsor_status == 'no' and len(
                        SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                    sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                    sponsored_product.delete()

                if sponsor_status == 'yes' and len(
                        SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                    sponsored_product = SponsoredProductForPrize(product=current_product_data)
                    sponsored_product.save()

                length_of_extra_imgs = len(extra_imgs)

                if policy == 'company':
                    if curnt_product_cat:
                        current_product_data.category = curnt_product_cat
                        current_product_data.save()
                    if curnt_product_subcat:
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.save()
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = "apcp"
                    current_product_data.return_policy = "apcp"
                    current_product_data.delivery_policy = "apcp"
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == 'own':
                    if curnt_product_cat:
                        current_product_data.category = curnt_product_cat
                        current_product_data.save()
                    if curnt_product_subcat:
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.save()
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == '':
                    if curnt_product_cat:
                        current_product_data.category = curnt_product_cat
                        current_product_data.save()
                    if curnt_product_subcat:
                        current_product_data.subcategory = curnt_product_subcat
                        current_product_data.save()
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()

                messages.success(request, "Successfully updated!")
                return redirect('apAllProductList')
            else:
                # removing/saving product from sponsored product prize list if sponsored status is false
                if sponsor_status == 'no' and len(
                        SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                    sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                    sponsored_product.delete()

                if sponsor_status == 'yes' and len(
                        SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                    sponsored_product = SponsoredProductForPrize(product=current_product_data)
                    sponsored_product.save()

                if policy == 'company':

                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = "apcp"
                    current_product_data.return_policy = "apcp"
                    current_product_data.delivery_policy = "apcp"
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == 'own':
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                if policy == '':
                    if curnt_product_cat:
                        current_product_data.category = curnt_product_cat
                    if curnt_product_subcat:
                        current_product_data.subcategory = curnt_product_subcat
                    current_product_data.title = title
                    current_product_data.brand_name = brand__name
                    current_product_data.regular_price = old_price
                    current_product_data.price = new_price
                    current_product_data.short_des = short_des
                    current_product_data.details = details
                    current_product_data.use_case = use_cases
                    current_product_data.benefits = benefits
                    current_product_data.security_policy = security_policy
                    current_product_data.return_policy = return_policy
                    current_product_data.delivery_policy = delivery_policy
                    current_product_data.store_name = store__name
                    current_product_data.store_link = store_link
                    current_product_data.about_store = about_store
                    current_product_data.in_stock = in_stock
                    current_product_data.policy_followed = policy
                    current_product_data.sponsor_status = sponsor_status
                    current_product_data.save()
                messages.success(request, "Successfully updated!")
                return redirect('apAllProductList')


    context = {
        'current_pk' : pk,
        'current_product_data' : current_product_data,
        'product_category' : product_category,
        'product_subcategory' : product_subcat,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product/update_product.html', context)


# gaming section starts *****************************************************************

# deactivating other segments while activating one segments
def deactivate_other_game_setting(obj):
    for x in obj:
        if x.status:
            x.status = False
            x.save()
    return True

@login_required(login_url='/ap/register/updated')
def ap_game_settings(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        # no_of_segments = request.POST.get('no_of_segments')
        no_spins = request.POST.get('no_spins')
        spin_duration = request.POST.get('spin_duration')
        config_status = request.POST.get('config_status')

        try:
            if config_status:
                # deactivating other segments while activating the current segment
                other_segment_obj = GameSetting.objects.all()
                thrding_deactivation_process = threading.Thread(target=deactivate_other_game_setting,
                                                                args=[other_segment_obj])
                thrding_deactivation_process.start()

                game_setting_model = GameSetting(
                    no_of_segments=5,
                    no_of_complt_spins=no_spins,
                    spining_duration=spin_duration,
                    status=config_status
                )
                game_setting_model.save()

                messages.success(request, "Successfully added!")
                return redirect('apGameSettings')
        except:
            messages.warning(request, "Can't be added! Try again!")
            return redirect('apGameSettings')

    # game setting list
    game_config_list = GameSetting.objects.all()

    context = {
        'game_config_list' : game_config_list,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/game/setting.html', context)


@login_required(login_url='/ap/register/updated')
def ap_activate_game_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = GameSetting.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()

        # deactivating other segments while activating the current segment
        other_segment_obj = GameSetting.objects.all().exclude(pk=pk)
        thrding_deactivation_process = threading.Thread(target=deactivate_other_game_setting, args=[other_segment_obj])
        thrding_deactivation_process.start()

        messages.success(request, "Successfully activated!")
        return redirect('apGameSettings')
    except:
        messages.warning(request, "Can't be activated! Try again!")
        return redirect('apGameSettings')

    return redirect('apGameSettings')


@login_required(login_url='/ap/register/updated')
def ap_deactivate_game_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = GameSetting.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()

        messages.success(request, "Successfully de-activated!")
        return redirect('apGameSettings')
    except:
        messages.warning(request, "Can't be de-activated! Try again!")
        return redirect('apGameSettings')

    return redirect('apGameSettings')


@login_required(login_url='/ap/register/updated')
def ap_update_game_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        # user profile picture
        profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

        current_obj = GameSetting.objects.get(pk=pk)

        if request.method == 'POST':
            # no_of_segments = request.POST.get('no_of_segments')
            no_spins = request.POST.get('no_spins')
            spin_duration = request.POST.get('spin_duration')
            config_status = request.POST.get('config_status')

            try:
                current_obj.no_of_segments = 5
                current_obj.no_of_complt_spins = no_spins
                current_obj.spining_duration = spin_duration
                current_obj.status = config_status
                current_obj.save()
                messages.success(request, "Successfully updated!")
                return redirect('apGameSettings')
            except:
                messages.warning(request, "Can't be updated! Try again!")
                return redirect('apGameSettings')

        context = {
            'current_obj' : current_obj,
            'currnt_pk' : pk,
            'profile_pic' : profile_pic,
        }
        return render(request, 'backEnd_superAdmin/game/update_game_segment.html', context)

    except:
        messages.warning(request, "Object not found! Try again!")
        return redirect('apGameSettings')

    return render(request, 'backEnd_superAdmin/game/update_game_segment.html')

@login_required(login_url='/ap/register/updated')
def ap_delete_game_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = GameSetting.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apGameSettings')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apGameSettings')

    return redirect('apGameSettings')


@login_required(login_url='/ap/register/updated')
def ap_segment_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        # user profile picture
        profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

        game__setting = GameSetting.objects.get(status=True)

        segments_list = Segment.objects.all()

        sponsored_products = SponsoredProductForPrize.objects.filter(status=True)

        if request.method == 'POST':
            segment = request.POST.get('segment_name')
            bg_color = request.POST.get('bg_color')
            prize_title = request.POST.get('prize_title')
            segment_prize__type = request.POST.get('segment_prize__type')
            point_as_prize = request.POST.get('point_as_prize')
            product_as_prize = request.POST.get('product_as_prize')
            segment_status = request.POST.get('segment_status')


            if segment and bg_color and segment_prize__type and segment_status and len(SegmentList.objects.filter(segment=Segment.objects.get(pk=segment))) <= 0:
                if segment_prize__type == 'product':
                    current_segment = Segment.objects.get(pk=segment)
                    current_prodct_as_prize = SponsoredProductForPrize.objects.get(pk=product_as_prize)

                    segment_list_model = SegmentList(segment=current_segment, bg_color=bg_color, prize_title=prize_title, segment_prize_type='1', product_as_prize=current_prodct_as_prize, status=segment_status)
                    segment_list_model.save()
                    messages.success(request, "Succesfully added!")
                    return redirect('apSegmentSettings')
                if segment_prize__type == 'point':
                    current_segment = Segment.objects.get(pk=segment)

                    segment_list_model = SegmentList(segment=current_segment, bg_color=bg_color, prize_title=prize_title, segment_prize_type='2', prize_point_amount=point_as_prize, status=segment_status)
                    segment_list_model.save()
                    messages.success(request, "Succesfully added!")
                    return redirect('apSegmentSettings')

            else:
                messages.warning(request, "This segment already exists!")
                return redirect('apSegmentSettings')

        segment_list_with_prizes = SegmentList.objects.all()

        context = {
            'segments': segments_list,
            'sponsored_products' : sponsored_products,
            'game__setting' : game__setting,
            'segment_list_with_prizes': segment_list_with_prizes,
            'profile_pic' : profile_pic,
        }
        return render(request, 'backEnd_superAdmin/game/segment_setting.html', context)
    except:
        messages.warning(request, "Number of segment is not specified. Please complete game setting or activate game configuration!")
        return redirect('apGameSettings')

    return render(request, 'backEnd_superAdmin/game/segment_setting.html')

@login_required(login_url='/ap/register/updated')
def ap_activate__segment(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SegmentList.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()
        messages.success(request, "This segment has been activated!")
        return redirect('apSegmentSettings')
    except:
        messages.warning(request, "This segment can't be activated! Try again!")
        return redirect('apSegmentSettings')

    return redirect('apSegmentSettings')

@login_required(login_url='/ap/register/updated')
def ap_deactivate__segment(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SegmentList.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()
        messages.success(request, "This segment has been de-activated!")
        return redirect('apSegmentSettings')
    except:
        messages.warning(request, "This segment can't be de-activated! Try again!")
        return redirect('apSegmentSettings')

    return redirect('apSegmentSettings')


@login_required(login_url='/ap/register/updated')
def ap_update_segment_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        # user profile picture
        profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

        current_obj = SegmentList.objects.get(pk=pk)

        segments_list = Segment.objects.all()

        sponsored_products = SponsoredProductForPrize.objects.all()

        if request.method == 'POST':
            segment = request.POST.get('segment_name')
            bg_color = request.POST.get('bg_color')
            prize_title = request.POST.get('prize_title')
            segment_prize__type = request.POST.get('segment_prize__type')
            point_as_prize = request.POST.get('point_as_prize')
            product_as_prize = request.POST.get('product_as_prize')
            segment_status = request.POST.get('segment_status')

            if segment and bg_color and segment_prize__type and segment_status:
                if segment_prize__type == 'product':
                    current_segment = Segment.objects.get(pk=segment)
                    current_prodct_as_prize = SponsoredProductForPrize.objects.get(pk=product_as_prize)

                    segment_list_model = SegmentList.objects.get(pk=pk)
                    segment_list_model.segment=current_segment
                    segment_list_model.bg_color=bg_color
                    segment_list_model.segment_prize_type='1'
                    segment_list_model.product_as_prize=current_prodct_as_prize
                    segment_list_model.status=segment_status
                    segment_list_model.prize_title = prize_title
                    segment_list_model.save()

                    messages.success(request, "Succesfully updated!")
                    return redirect('apSegmentSettings')

                if segment_prize__type == 'point':
                    current_segment = Segment.objects.get(pk=segment)

                    segment_list_model = SegmentList.objects.get(pk=pk)
                    segment_list_model.segment=current_segment
                    segment_list_model.bg_color=bg_color
                    segment_list_model.segment_prize_type='2'
                    segment_list_model.prize_point_amount=point_as_prize
                    segment_list_model.status=segment_status
                    segment_list_model.prize_title = prize_title
                    segment_list_model.save()

                    messages.success(request, "Succesfully updated!")
                    return redirect('apSegmentSettings')

        context = {
            'segments': segments_list,
            'sponsored_products': sponsored_products,
            'current_obj' : current_obj,
            'current_pk': pk,
            'profile_pic' : profile_pic,
        }
        return render(request, 'backEnd_superAdmin/game/update_segment_setting.html', context)
    except:
        pass

    return render(request, 'backEnd_superAdmin/game/update_segment_setting.html')


@login_required(login_url='/ap/register/updated')
def ap_del_segment_setting(request,pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SegmentList.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apSegmentSettings')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apSegmentSettings')

    return redirect('apSegmentSettings')

@login_required(login_url='/ap/register/updated')
def ap_sponsored_prdacts_for_game(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    sponsored_product_list = SponsoredProductForPrize.objects.all()

    context = {
        'profile_pic' : profile_pic,
        'sponsored_product_list' : sponsored_product_list,
    }

    return render(request, 'backEnd_superAdmin/game/sponsored_prdct_list.html', context)


@login_required(login_url='/ap/register/updated')
def ap_add_new_segment(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        name = request.POST.get('segment_name')

        print(name)

        if name and len(Segment.objects.filter(name=name)) <= 0:
            segment_model = Segment.objects.create(name=name)
            messages.success(request, "Successfully added!")
            return redirect('apAddNewSegment')
        else:
            messages.warning(request, "Can't be added!")
            return redirect('apAddNewSegment')

    # segments list
    segments_list = Segment.objects.all()

    context = {
        'segments_list': segments_list,
    }

    return render(request, 'backEnd_superAdmin/game/add_segment.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_new_segment(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = Segment.objects.filter(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddNewSegment')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddNewSegment')

    return redirect('apAddNewSegment')


# deactivate other sponsored product for winning chance
# def deactivateOtherProductFor_winning_chance(obj):
#
#     if obj:
#         for x in obj:
#             x.status = False
#             x.save()
#     return True

@login_required(login_url='/ap/register/updated')
def ap_activate_spnsored_prdct_for_game(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SponsoredProductForPrize.objects.get(pk=pk)
        current_obj.status = True
        current_obj.prodct_id = get_random_string(8)
        current_obj.save()

        # threading de-activation process
        # other_active_products = SponsoredProductForPrize.objects.filter(status=True).exclude(pk=pk)
        # de_activate_other_prdcts = threading.Thread(target=deactivateOtherProductFor_winning_chance, args=[other_active_products])
        # de_activate_other_prdcts.start()

        messages.success(request, "This product has been activated for game to win!")
        return redirect('apGameSponsoredProducts')
    except:
        messages.warning(request, "This item can't be activated! Try again!")
        return redirect('apGameSponsoredProducts')
    return redirect('apGameSponsoredProducts')


@login_required(login_url='/ap/register/updated')
def ap_deactivate_sponsord_prdct_for_game(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SponsoredProductForPrize.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()

        messages.success(request, "This product has been de-activated for game to win!")
        return redirect('apGameSponsoredProducts')
    except:
        messages.warning(request, "This item can't be de-activated! Try again!")
        return redirect('apGameSponsoredProducts')

    return redirect('apGameSponsoredProducts')

@login_required(login_url='/ap/register/updated')
def ap_del_sponsored_product(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SponsoredProductForPrize.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apGameSponsoredProducts')
    except:
        messages.warning(request, "Object not found! Try again!")
        return redirect('apGameSponsoredProducts')

    return redirect('apGameSponsoredProducts')


# add applicable rules for prize winner
@login_required(login_url='/ap/register/updated')
def ap_applicable_rules_for_prize_winner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # sponsored product list
    sponsored_product_list = SponsoredProductForPrize.objects.all()

    if request.method == 'POST':
        product_pk = request.POST.get('product')
        rules = request.POST.get('applicable_rules')

        if product_pk and rules:
            product = SponsoredProductForPrize.objects.filter(pk=product_pk).first()
            applicable_rules_model = ApplicableRulesForWinner.objects.create(user=request.user, product=product, applicable_rules=rules)
            messages.success(request, "Successfully added!")
            return redirect('apApplicableRuleWinningPrize')

        else:
            messages.warning(request, "Can't be added! Try again!")
            return redirect('apApplicableRuleWinningPrize')

    # product list with applicable rules
    product_list_with_app_rules = ApplicableRulesForWinner.objects.all()

    context = {
        'sponsored_product_list': sponsored_product_list,
        'product_list_with_app_rules' : product_list_with_app_rules,
    }

    return render(request, 'backEnd_superAdmin/game/applicable_rules_setting_for_winner.html', context)


@login_required(login_url='/ap/register/updated')
def ap_remove_prduct_with_applicable_rules(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        product = ApplicableRulesForWinner.objects.get(pk=pk)
        product.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apApplicableRuleWinningPrize')
    except:
        messages.warning(request, "can't be deleted! Try again please!")
        return redirect('apApplicableRuleWinningPrize')

    return redirect('apApplicableRuleWinningPrize')
# gaming section starts ends *****************************************************************


# accounts section *********************************************************
@login_required(login_url='/ap/register/updated')
def ap_seller_accounts_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    seller_list = Account.objects.filter(Q(is_seller=True) & Q(status='1'))

    context = {
        'profile_pic' : profile_pic,
        'seller_list' : seller_list,
    }

    return render(request, 'backEnd_superAdmin/accounts/seller_accounts_list.html', context)


@login_required(login_url='/ap/register/updated')
def ap_buyer_accounts_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    buyer_list = Account.objects.filter(Q(is_buyer=True) & Q(status='1'))

    context = {
        'buyer_list': buyer_list,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/accounts/buyer_accounts_list.html', context)


@login_required(login_url='/ap/register/updated')
def ap_staff_accounts_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    staff_list = Account.objects.filter(Q(is_a_staff=True) & Q(status='1'))

    context = {
        'staff_list': staff_list,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/accounts/staff_accounts_list.html', context)

# settings section ************************************************************
@login_required(login_url='/ap/register/updated')
def ap_add_site_logo(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        logo = request.FILES['logo']

        if logo and SiteLogo.objects.count() <= 0:
            logo_model = SiteLogo(logo=logo)
            logo_model.save()
            messages.success(request, "Successfully added!")
            return redirect('apAddSiteLogo')
        else:
            messages.warning(request, "Logo already exists! Delete existing one to add new logo!")
            return redirect('apAddSiteLogo')

    # existing logo
    existing_logo = SiteLogo.objects.filter().first()

    context = {
        'existing_logo': existing_logo,
    }

    return render(request, 'backEnd_superAdmin/site_setting/logo/add_logo.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_site_logo(request, pk):

    try:
        fs = FileSystemStorage()
        current_obj = SiteLogo.objects.get(pk=pk)
        fs.delete(current_obj.logo.name)

        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAddSiteLogo')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddSiteLogo')

    return redirect('apAddSiteLogo')

# top footer section starts***********************************************************
@login_required(login_url='/ap/register/updated')
def ap_top_footer_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # free delivery setting
    free_delivery_setting = FreeDelivery.objects.filter().first()

    # safe payment
    safe_payment_setting = SafePayment.objects.filter().first()

    # free delivery setting
    shop_with_confidence = ShopWithConfidence.objects.filter().first()

    # safe payment
    help_center = HelpCenter.objects.filter().first()

    context = {
        'free_delivery_setting' : free_delivery_setting,
        'safe_payment_setting' : safe_payment_setting,
        'shop_with_confidence' : shop_with_confidence,
        'help_center' : help_center,
    }

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html', context)

@login_required(login_url='/ap/register/updated')
def ap_free_delivery_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        des = request.POST.get('short_description')

        if des and FreeDelivery.objects.count() <= 0:
            free_delivery_model = FreeDelivery.objects.create(des=des)
            messages.success(request, "Successfully added!")
            return redirect('apTopFooterSetting')
        else:
            messages.warning(request, "Can't be added! Delete the current Object to add new one!")
            return redirect('apTopFooterSetting')

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html')

@login_required(login_url='/ap/register/updated')
def ap_del_free_delivery_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = FreeDelivery.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apTopFooterSetting')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apTopFooterSetting')

    return redirect('apTopFooterSetting')

@login_required(login_url='/ap/register/updated')
def ap_add_safe_payment_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        des = request.POST.get('short_description')

        if des and SafePayment.objects.count() <= 0:
            safe_payment_model = SafePayment.objects.create(des=des)
            messages.success(request, "Successfully added!")
            return redirect('apTopFooterSetting')
        else:
            messages.warning(request, "Can't be added! Delete the current Object to add new one!")
            return redirect('apTopFooterSetting')

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html')

@login_required(login_url='/ap/register/updated')
def ap_del_safe_payment_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = SafePayment.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apTopFooterSetting')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apTopFooterSetting')

    return redirect('apTopFooterSetting')

# jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
@login_required(login_url='/ap/register/updated')
def ap_shop_with_confident_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        des = request.POST.get('short_description')

        if des and ShopWithConfidence.objects.count() <= 0:
            shop_with_confident_model = ShopWithConfidence.objects.create(des=des)
            messages.success(request, "Successfully added!")
            return redirect('apTopFooterSetting')
        else:
            messages.warning(request, "Can't be added! Delete the current Object to add new one!")
            return redirect('apTopFooterSetting')

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html')

@login_required(login_url='/ap/register/updated')
def ap_del_shop_with_confident_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = ShopWithConfidence.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apTopFooterSetting')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apTopFooterSetting')

    return redirect('apTopFooterSetting')

@login_required(login_url='/ap/register/updated')
def ap_add_help_center_setting(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        des = request.POST.get('short_description')

        if des and HelpCenter.objects.count() <= 0:
            help_model = HelpCenter.objects.create(des=des)
            messages.success(request, "Successfully added!")
            return redirect('apTopFooterSetting')
        else:
            messages.warning(request, "Can't be added! Delete the current Object to add new one!")
            return redirect('apTopFooterSetting')

    return render(request, 'backEnd_superAdmin/site_setting/top_footer.html')

@login_required(login_url='/ap/register/updated')
def ap_del_help_center_setting(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HelpCenter.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apTopFooterSetting')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apTopFooterSetting')

    return redirect('apTopFooterSetting')

# top footer section ends************************************************************

@login_required(login_url='/ap/register/updated')
def ap_about_us(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        content = request.POST['about_us']

        try:
            if content and AboutUs.objects.count() == 0:
                about_us_model = AboutUs(about_us=content)
                about_us_model.save()
                messages.success(request, "Successfully added!")
                return redirect('apAboutUs')
            else:
                messages.warning(request, "Already exists! Try to edit or delete existing info!")
                return redirect('apAboutUs')
        except:
            messages.warning(request, "Already exists! Try to edit or delete existing info!")
            return redirect('apAboutUs')

    # about us content
    about_us_content = AboutUs.objects.filter().first()

    context = {
        'about_us': about_us_content,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/site_setting/about_us.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_about_us(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = AboutUs.objects.get(pk=pk)
        obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apAboutUs')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAboutUs')

    return redirect('apAboutUs')

@login_required(login_url='/ap/register/updated')
def ap_edit_about_us(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = AboutUs.objects.get(pk=pk)

    if request.method == 'POST':
        content = request.POST['about_us']

        try:
            if content:
                current_obj.about_us = content
                current_obj.save()
                messages.success(request, "Successfully updated!")
                return redirect('apAboutUs')
            else:
                messages.warning(request, "Something wrong! Try again!")
                return redirect('apAboutUs')
        except:
            messages.warning(request, "Something wrong! Try again!")
            return redirect('apAboutUs')


    context = {
        'profile_pic' : profile_pic,
        'obj_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/site_setting/edit_about_us.html', context)

# contact us section ********************************************************
@login_required(login_url='/ap/register/updated')
def ap_contact_us(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        short_qoute = request.POST['short_qoute']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        mobile = request.POST['mobile']
        hotline = request.POST['hotline']
        email = request.POST['email']
        email2 = request.POST['email2']

        try:
            if short_qoute and address_line_1 and mobile and email and ContactUs.objects.count() == 0:
                contact_us_model = ContactUs(
                    short_qoute=short_qoute,
                    address_line_one=address_line_1,
                    address_line_two=address_line_2,
                    mobile=mobile,
                    hotline=hotline,
                    email_one=email,
                    email_two=email2
                )
                contact_us_model.save()
                messages.success(request, "Successfully added!")
                return redirect('apcontactUs')
            else:
                messages.warning(request, "Already exists! Try to edit or delete existing info!")
                return redirect('apcontactUs')
        except:
            messages.warning(request, "Already exists! Try to edit or delete existing info!")
            return redirect('apcontactUs')

    # about us content
    contact_us_obj = ContactUs.objects.filter().first()

    context = {
        'contact_us': contact_us_obj,
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/site_setting/contact-us/contact-us.html', context)

@login_required(login_url='/ap/register/updated')
def ap_edit_contact_us(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = ContactUs.objects.get(pk=pk)

    if request.method == 'POST':
        short_qoute = request.POST['short_qoute']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        mobile = request.POST['mobile']
        hotline = request.POST['hotline']
        email = request.POST['email']
        email2 = request.POST['email2']

        try:
            if short_qoute and address_line_1 and mobile and email:
                current_obj.short_qoute = short_qoute
                current_obj.address_line_one = address_line_1
                current_obj.address_line_two = address_line_2
                current_obj.mobile = mobile
                current_obj.hotline = hotline
                current_obj.email_one = email
                current_obj.email_two = email2
                current_obj.save()
                messages.success(request, "Successfully updated!")
                return redirect('apcontactUs')
            else:
                messages.warning(request, "Something wrong! Try again!")
                return redirect('apcontactUs')
        except:
            messages.warning(request, "Something wrong! Try again!")
            return redirect('apcontactUs')


    context = {
        'profile_pic' : profile_pic,
        'obj_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/site_setting/contact-us/edit_contact_us.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_contact_us(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = ContactUs.objects.get(pk=pk)
        obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apcontactUs')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAboutUs')

    return redirect('apcontactUs')


# policy setting ***************************************************************


@login_required(login_url='/ap/register/updated')
def ap_delivery_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        delivery_policy = request.POST['delivery_policy']

        try:
            if delivery_policy and DeliveryPolicy.objects.count() == 0:
                delvery_model = DeliveryPolicy(content=delivery_policy)
                delvery_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apDeliveryPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apDeliveryPolicy')

    # delivery policy list
    current_delivery_policy = DeliveryPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'current_delivery_policy' : current_delivery_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/delivery_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_delivery_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = DeliveryPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        delivery_policy = request.POST['delivery_policy']

        try:
            if delivery_policy:
                current_obj.content = delivery_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apDeliveryPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apDeliveryPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_delivery_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_delivery_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = DeliveryPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apDeliveryPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apDeliveryPolicy')

    return redirect('apDeliveryPolicy')


# return policy
@login_required(login_url='/ap/register/updated')
def ap_add_return_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        return_policy = request.POST['return_policy']

        try:
            if return_policy and ReturnPolicy.objects.count() == 0:
                return_model = ReturnPolicy(content=return_policy)
                return_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddReturnPolicy')
            else:
                messages.warning(request, 'Already exists! Try again!')
                return redirect('apAddReturnPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddReturnPolicy')

    # return policy list
    current_return_policy = ReturnPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'current_return_policy' : current_return_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/return_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_return_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = ReturnPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        return_policy = request.POST['return_policy']

        try:
            if return_policy:
                current_obj.content = return_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddReturnPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddReturnPolicy')

    context = {
        'profile_pic': profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_return_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_return_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = ReturnPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddReturnPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddReturnPolicy')

    return redirect('apAddReturnPolicy')


# product refund policy
@login_required(login_url='/ap/register/updated')
def ap_add_refund_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        refund_policy = request.POST['refund_policy']

        try:
            if refund_policy and RefundPolicy.objects.count() == 0:
                refund_policy_model = RefundPolicy(content=refund_policy)
                refund_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddRefundPolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddRefundPolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddRefundPolicy')

    # return policy list
    current_refund_policy = RefundPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'current_refund_policy' : current_refund_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/refund_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_refund_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = RefundPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        refund_policy = request.POST['refund_policy']

        try:
            if refund_policy:
                current_obj.content = refund_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddRefundPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddRefundPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_refund_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_refund_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = RefundPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddRefundPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddRefundPolicy')

    return redirect('apAddRefundPolicy')

# product security
@login_required(login_url='/ap/register/updated')
def ap_add_security_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        security_policy = request.POST['security_policy']

        try:
            if security_policy and SecurityPolicy.objects.count() == 0:
                security_policy_model = SecurityPolicy(content=security_policy)
                security_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddSecurityPolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddSecurityPolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddSecurityPolicy')

    # security policy list
    current_security_policy = SecurityPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'current_security_policy' : current_security_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/security_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_security_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = SecurityPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        security_policy = request.POST['security_policy']

        try:
            if security_policy:
                current_obj.content = security_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddSecurityPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddSecurityPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_security_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_security_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = SecurityPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddSecurityPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddSecurityPolicy')

    return redirect('apAddSecurityPolicy')


# terms & conditions policy
@login_required(login_url='/ap/register/updated')
def ap_add_termCondition_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        terms_condition_policy = request.POST['terms_condition_policy']

        try:
            if terms_condition_policy and TermsConditions.objects.count() == 0:
                terms_condition_policy_model = TermsConditions(content=terms_condition_policy)
                terms_condition_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddTermsConditionPolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddTermsConditionPolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddTermsConditionPolicy')

    # security policy list
    currnt_terms_condition_policy = TermsConditions.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'currnt_terms_condition_policy' : currnt_terms_condition_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/terms_condition.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_termCondition_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = TermsConditions.objects.get(pk=pk)

    if request.method == 'POST':
        terms_condition_policy = request.POST['terms_condition_policy']

        try:
            if terms_condition_policy:
                current_obj.content = terms_condition_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddTermsConditionPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddTermsConditionPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_terms_condition.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_termCondition_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = TermsConditions.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddTermsConditionPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddTermsConditionPolicy')

    return redirect('apAddTermsConditionPolicy')


# product privacy policy
@login_required(login_url='/ap/register/updated')
def ap_add_ProductPrivacy_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        product_privacy_policy = request.POST['product_privacy_policy']

        try:
            if product_privacy_policy and PrivacyPolicy.objects.count() == 0:
                product_privacy_policy_model = PrivacyPolicy(content=product_privacy_policy)
                product_privacy_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddProductPrivacyPolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddProductPrivacyPolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddProductPrivacyPolicy')

    # security policy list
    currnt_privacy_policy = PrivacyPolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'currnt_privacy_policy' : currnt_privacy_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/add_product_privacy_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_ProductPrivacy_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = PrivacyPolicy.objects.get(pk=pk)

    if request.method == 'POST':
        product_privacy_policy = request.POST['product_privacy_policy']

        try:
            if product_privacy_policy:
                current_obj.content = product_privacy_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddProductPrivacyPolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddProductPrivacyPolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_add_product_privacy_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_ProductPrivacy_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = PrivacyPolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddProductPrivacyPolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddProductPrivacyPolicy')

    return redirect('apAddProductPrivacyPolicy')


# cookie policy
@login_required(login_url='/ap/register/updated')
def ap_add_cookie_policy(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        cookie_policy = request.POST['cookie_policy']

        try:
            if cookie_policy and CookiePolicy.objects.count() == 0:
                cookie_policy_model = CookiePolicy(content=cookie_policy)
                cookie_policy_model.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddCookiePolicy')
            else:
                messages.warning(request, 'Already exists! Update or delete existing one!')
                return redirect('apAddCookiePolicy')
        except:
            messages.warning(request, 'Already exists! Update or delete existing one!')
            return redirect('apAddCookiePolicy')

    # security policy list
    currnt_cookie_policy = CookiePolicy.objects.filter().first()

    context = {
        'profile_pic' : profile_pic,
        'currnt_cookie_policy' : currnt_cookie_policy,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/add_cookie_policy.html', context)

@login_required(login_url='/ap/register/updated')
def ap_update_cookie_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_obj = CookiePolicy.objects.get(pk=pk)

    if request.method == 'POST':
        cookie_policy = request.POST['cookie_policy']

        try:
            if cookie_policy:
                current_obj.content = cookie_policy
                current_obj.save()
                messages.success(request, 'Successfully added!')
                return redirect('apAddCookiePolicy')
        except:
            messages.warning(request, 'Something wrong! Try again!')
            return redirect('apAddCookiePolicy')

    context = {
        'profile_pic' : profile_pic,
        'current_pk' : pk,
        'current_obj' : current_obj,
    }

    return render(request, 'backEnd_superAdmin/policy_setting/update_add_cookie_policy.html', context)


@login_required(login_url='/ap/register/updated')
def ap_del_cookie_policy(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        obj = CookiePolicy.objects.get(pk=pk)
        obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('apAddCookiePolicy')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apAddCookiePolicy')

    return redirect('apAddCookiePolicy')

# profile settings **************************************************************
@login_required(login_url='/ap/register/updated')
def ap_my_profile(request, username):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    context = {
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/profile/my-profile.html', context)


# banner section starts ******************************************************************

# Home page main banner
@login_required(login_url='/ap/register/updated')
def ap_add_banner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        offer_title = request.POST.get('offer_title')
        offer_title_amnt = request.POST.get('offer_title_amnt')
        offer_duration = request.POST.get('offer_duration')
        prduct_title = request.POST.get('prduct_title')
        price = request.POST.get('price')
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        if banner_img and url:
            banner_id = uuid.uuid4()

            banner_model = BannerList(
                banner_id=banner_id,
                user=request.user,
                offer_title=offer_title,
                offer_amount_or_title=offer_title_amnt,
                offer_duration=offer_duration,
                product_title=prduct_title,
                starting_price=price,
                img=banner_img,
                product_url=url
            )
            banner_model.save()
            messages.success(request, "New banner has been added successfully!")
            return redirect('apAddBanner')

    context = {
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/banner_section/add_banner.html', context)


@login_required(login_url='/ap/register/updated')
def ap_update_banner(request, pk, banner_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_banner = BannerList.objects.get(pk=pk)

    if request.method == 'POST':
        offer_title = request.POST.get('offer_title')
        offer_title_amnt = request.POST.get('offer_title_amnt')
        offer_duration = request.POST.get('offer_duration')
        prduct_title = request.POST.get('prduct_title')
        price = request.POST.get('price')
        url = request.POST.get('url')

        try:
            fs = FileSystemStorage()
            banner_img = request.FILES['banner_img']

            if banner_img:
                # deleting current banner image
                fs.delete(current_banner.img.name)

                current_banner.offer_title = offer_title
                current_banner.offer_amount_or_title = offer_title_amnt
                current_banner.offer_duration = offer_duration
                current_banner.product_title = prduct_title
                current_banner.starting_price = price
                current_banner.img = banner_img
                current_banner.product_url = url
                current_banner.save()
                messages.success(request, "Successfully updated!")
                return redirect('apBannerList')
        except:
            current_banner.offer_title = offer_title
            current_banner.offer_amount_or_title = offer_title_amnt
            current_banner.offer_duration = offer_duration
            current_banner.product_title = prduct_title
            current_banner.starting_price = price
            current_banner.product_url = url
            current_banner.save()
            messages.success(request, "Successfully updated!")
            return redirect('apBannerList')
    context = {
        'profile_pic' : profile_pic,
        'current_banner': current_banner,
        'current_pk': pk,
        'banner_id': banner_id,
    }

    return render(request, 'backEnd_superAdmin/banner_section/update_banner.html', context)


@login_required(login_url='/ap/register/updated')
def ap_banner_details(request, pk, banner_id):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    current_banner = BannerList.objects.get(pk=pk)

    context = {
        'profile_pic' : profile_pic,
        'current_banner': current_banner,
        'current_pk': pk,
        'banner_id': banner_id,
    }

    return render(request, 'backEnd_superAdmin/banner_section/banner_details.html', context)

@login_required(login_url='/ap/register/updated')
def ap_banner_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    banner_list = BannerList.objects.all()

    context = {
        'profile_pic' : profile_pic,
        'banner_list' : banner_list,
    }

    return render(request, 'backEnd_superAdmin/banner_section/banner_list.html', context)


# home page mini top banner
@login_required(login_url='/ap/register/updated')
def ap_home_pageMini_topBanner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        bnr_id = uuid.uuid4()

        if banner_img and url:
            mini_top_bnr = HomeMiniTopBanner.objects.create(banner_id=bnr_id, user=request.user, img=banner_img, url=url)
            messages.success(request, "Successfully added!")
            return redirect('apAddHomePageMiniTopBanner')
        else:
            messages.warning(request, "Can't be added! Try again!")
            return redirect('apAddHomePageMiniTopBanner')

    return render(request, 'backEnd_superAdmin/mini_home_page_slider/add_to_mini_top_slider.html')


@login_required(login_url='/ap/register/updated')
def ap_home_pageMini_topBanrList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    home_top_bnr_list = HomeMiniTopBanner.objects.all()
    context = {
        'home_top_slider_list': home_top_bnr_list,
    }

    return render(request, 'backEnd_superAdmin/mini_home_page_slider/mini_top_slider_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_activate_home_pageMini_topBanr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniTopBanner.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()
        messages.success(request, "Successfully activated!")
        return redirect('apHomePageMiniTopBannerList')

    except:
        messages.warning(request, "Can't be activated! Try again!")
        return redirect('apHomePageMiniTopBannerList')

    return redirect('apHomePageMiniTopBannerList')

@login_required(login_url='/ap/register/updated')
def ap_de_activate_home_pageMini_topBanr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniTopBanner.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()
        messages.success(request, "Successfully de-activated!")
        return redirect('apHomePageMiniTopBannerList')

    except:
        messages.warning(request, "Can't be de-activated! Try again!")
        return redirect('apHomePageMiniTopBannerList')

    return redirect('apHomePageMiniTopBannerList')

@login_required(login_url='/ap/register/updated')
def ap_delete_home_pageMiniTopBanner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniTopBanner.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(current_obj.img.name)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apHomePageMiniTopBannerList')
    except:
        messages.warning(request, "Can't deleted!")
        return redirect('apHomePageMiniTopBannerList')

    return redirect('apHomePageMiniTopBannerList')


# home page mini bottom banner
@login_required(login_url='/ap/register/updated')
def ap_home_pageMini_bottomBanner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    if request.method == 'POST':
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        bnr_id = uuid.uuid4()

        if banner_img and url:
            mini_top_bnr = HomeMiniBottomBanner.objects.create(banner_id=bnr_id, user=request.user, img=banner_img, url=url)
            messages.success(request, "Successfully added!")
            return redirect('apAddHomePageMiniTopBanner')
        else:
            messages.warning(request, "Can't be added! Try again!")
            return redirect('apAddHomePageMiniTopBanner')

    return render(request, 'backEnd_superAdmin/mini_home_page_slider/add_to_mini_bottom_slider.html')


@login_required(login_url='/ap/register/updated')
def ap_home_pageMini_BottomBanrList(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    home_bottom_bnr_list = HomeMiniBottomBanner.objects.all()

    context = {
        'home_bottom_bnr_list': home_bottom_bnr_list,
    }

    return render(request, 'backEnd_superAdmin/mini_home_page_slider/mini_bottom_slider_list.html', context)


@login_required(login_url='/ap/register/updated')
def ap_activate_home_pageMini_BottomBanr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniBottomBanner.objects.get(pk=pk)
        current_obj.status = True
        current_obj.save()
        messages.success(request, "Successfully activated!")
        return redirect('apHomePageMiniBottomBannerList')

    except:
        messages.warning(request, "Can't be activated! Try again!")
        return redirect('apHomePageMiniBottomBannerList')

    return redirect('apHomePageMiniBottomBannerList')


@login_required(login_url='/ap/register/updated')
def ap_de_activate_home_pageMini_bottomBanr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniBottomBanner.objects.get(pk=pk)
        current_obj.status = False
        current_obj.save()
        messages.success(request, "Successfully de-activated!")
        return redirect('apHomePageMiniBottomBannerList')

    except:
        messages.warning(request, "Can't be de-activated! Try again!")
        return redirect('apHomePageMiniBottomBannerList')

    return redirect('apHomePageMiniBottomBannerList')

@login_required(login_url='/ap/register/updated')
def ap_delete_home_pageMiniBottomBanner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = HomeMiniBottomBanner.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(current_obj.img.name)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apHomePageMiniBottomBannerList')
    except:
        messages.warning(request, "Can't deleted!")
        return redirect('apHomePageMiniBottomBannerList')

    return redirect('apHomePageMiniBottomBannerList')


@login_required(login_url='/ap/register/updated')
def ap_del_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        current_obj = BannerList.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(current_obj.img.name)

        current_obj.delete()
        messages.success(request, "Banner has been deleted!")
        return redirect('apBannerList')

    except:
        messages.warning(request, "Banner can't be deleted! Try again!")
        return redirect('apBannerList')

    return redirect('apBannerList')



# advertisement section
@login_required(login_url='/ap/register/updated')
def ap_add_banner_at_prod_detail_page(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        if banner_img and url:
            banner_id = uuid.uuid4()

            banner_model = BannerProdDetail.objects.create(
                banner_id=banner_id,
                user=request.user,
                img=banner_img,
                link=url
            )
            messages.success(request, "New banner has been added successfully!")
            return redirect('apAddBnrProdDetialPg')

    context = {
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/product_details_page_bannr/add_banner.html', context)


@login_required(login_url='/ap/register/updated')
def ap_prod_details_pg_banner_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    banner_list = BannerProdDetail.objects.all()

    context = {
        'profile_pic' : profile_pic,
        'banner_list' : banner_list,
    }

    return render(request, 'backEnd_superAdmin/product_details_page_bannr/banner_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_prod_details_pg_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        fs = FileSystemStorage()
        banner = BannerProdDetail.objects.get(pk=pk)
        fs.delete(banner.img.name)
        banner.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apProductDetailsPgBnrList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apProductDetailsPgBnrList')
    return redirect('apProductDetailsPgBnrList')

def deactivate_product_detail_pg_bnr(banner_list):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    for banner in banner_list:
        banner.status = False
        banner.save()

    return True

@login_required(login_url='/ap/register/updated')
def ap_activate_prod_details_pg_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        banner = BannerProdDetail.objects.get(pk=pk)

        other_banners = BannerProdDetail.objects.filter().exclude(pk=pk)
        banner.status = True
        banner.save()

        # theading deaactivate other banners
        thread = threading.Thread(target=deactivate_product_detail_pg_bnr, args=[other_banners])
        thread.start()

        messages.success(request, "Banner has been activated!")
        return redirect('apProductDetailsPgBnrList')
    except:
        messages.warning(request, "Can't be actiavated! Try again!")
        return redirect('apProductDetailsPgBnrList')

    return redirect('apProductDetailsPgBnrList')

@login_required(login_url='/ap/register/updated')
def ap_de_activate_prod_details_pg_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        banner = BannerProdDetail.objects.get(pk=pk)
        banner.status = False
        banner.save()

        messages.success(request, "Banner has been de-activated!")
        return redirect('apProductDetailsPgBnrList')
    except:
        messages.warning(request, "Can't be de-actiavated! Try again!")
        return redirect('apProductDetailsPgBnrList')

    return redirect('apProductDetailsPgBnrList')


# banner on shop page
@login_required(login_url='/ap/register/updated')
def ap_add_shop_page_banner(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        banner_img = request.FILES['banner_img']
        url = request.POST.get('url')

        banner_id = uuid.uuid4()

        if banner_img and url:
            shopPageBanner_model = ShopPageBanner.objects.create(banner_id=banner_id, user=request.user, img=banner_img, link=url)
            messages.success(request, "Successfully added new banner!")
            return redirect('apAddShopPageBanner')
        else:
            messages.warning(request, "Can't be added new banner! Try once again!")
            return redirect('apAddShopPageBanner')

    context = {
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd_superAdmin/banner_shop_page/add_banner.html', context)

@login_required(login_url='/ap/register/updated')
def ap_shop_page_banner_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    shop_page_banner_list = ShopPageBanner.objects.all()

    context = {
        'profile_pic': profile_pic,
        'shop_page_banner_list': shop_page_banner_list,
    }

    return render(request, 'backEnd_superAdmin/banner_shop_page/banner_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_delete_shop_page_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        fs = FileSystemStorage()
        current_obj = ShopPageBanner.objects.get(pk=pk)
        fs.delete(current_obj.img.name)
        current_obj.delete()
        messages.success(request, "Banner has been successfully deleted!")
        return redirect('apShopPageBannerList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apShopPageBannerList')

    return redirect('apShopPageBannerList')

def deactivate_shop_page_banner(banner_list):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    for banner in banner_list:
        banner.status = False
        banner.save()

    return True

@login_required(login_url='/ap/register/updated')
def ap_activate_shop_page_bannr(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        banner = ShopPageBanner.objects.get(pk=pk)

        other_banners = ShopPageBanner.objects.filter().exclude(pk=pk)
        banner.status = True
        banner.save()

        # theading deaactivate other banners
        thread = threading.Thread(target=deactivate_shop_page_banner, args=[other_banners])
        thread.start()

        messages.success(request, "Banner has been activated!")
        return redirect('apShopPageBannerList')
    except:
        messages.warning(request, "Can't be actiavated! Try again!")
        return redirect('apShopPageBannerList')

    return redirect('apShopPageBannerList')

@login_required(login_url='/ap/register/updated')
def ap_de_activate_shop_page_banner(request, pk):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    try:
        banner = ShopPageBanner.objects.get(pk=pk)
        banner.status = False
        banner.save()

        messages.success(request, "Banner has been de-activated!")
        return redirect('apShopPageBannerList')
    except:
        messages.warning(request, "Can't be de-actiavated! Try again!")
        return redirect('apProductDetailsPgBnrList')

    return redirect('apShopPageBannerList')


@login_required(login_url='/ap/register/updated')
def ap_subscriber_list(request):

    if request.user.is_admin != True:
        return redirect('frontEndLoginUser')

    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    subscriber_list = SubscriberList.objects.all()

    context = {
        'subscriber_list': subscriber_list,
        'profile_pic': profile_pic,
    }

    return render(request, 'backEnd_superAdmin/subscriber/subscriber_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_remove_subscriber(request, pk):

    try:
        current_obj = SubscriberList.objects.get(pk=pk)
        current_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apSubscriberList')

    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apSubscriberList')

    return redirect('apSubscriberList')

@login_required(login_url='/ap/register/updated')
def ap_customer_msg_list(request):
    # user profile picture
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()

    msg_list = CustomerMessageList.objects.all()

    context = {
        'profile_pic': profile_pic,
        'msg_list' : msg_list,
    }

    return render(request, 'backEnd_superAdmin/message_list.html', context)

@login_required(login_url='/ap/register/updated')
def ap_del_customer_msg(request, pk):

    try:
        currn_obj = CustomerMessageList.objects.get(pk=pk)
        currn_obj.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('apCustomerMessageList')
    except:
        messages.warning(request, "Can't be deleted! Try again!")
        return redirect('apCustomerMessageList')
    return redirect('apCustomerMessageList')