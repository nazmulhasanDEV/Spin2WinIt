import json

from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from product.models import *
from game.models import *
from adminPanel.models import *
from user.models import *
from verification.models import *
from core.models import *
from django.http import JsonResponse
import uuid
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='/fe/login/register')
def seller_dashboard_index(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    context = {

    }
    return render(request, 'backEnd__sellerDashboard/index.html', context)


@login_required(login_url='/fe/login/register')
def seller_dashboard_home(request, username):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # existing package list
    package_list = PackageList.objects.all()


    context = {
        'username': username,
        'package_list': package_list,
    }

    return render(request, 'backEnd__sellerDashboard/home.html', context)

@login_required(login_url='/fe/login/register')
def seller_add_product(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    product_cat = ProductCategory.objects.all()
    product_subcat = ProductSubCategory.objects.all()

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
        curnt_product_cat = ProductCategory.objects.get(pk=category)
        curnt_product_subcat = None
        if sub_category:
            curnt_product_subcat = ProductSubCategory.objects.get(pk=sub_category)


        try:
            extra_imgs = request.FILES.getlist('product__extra__images')
            length_of_extra_imgs = len(extra_imgs)

            if length_of_extra_imgs >= 0:
                for img in extra_imgs:
                    product_img_model = ProductImg.objects.create(product_id=product_id, product_type='mcp', img=img)

                if policy == 'company':
                    product_list_model = ProductList(
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
                        security_policy="apcp",
                        return_policy="apcp",
                        delivery_policy="apcp",
                        store_name=store__name,
                        store_link=store_link,
                        about_store=about_store,
                        in_stock=in_stock,
                        policy_followed=policy,
                        sponsor_status=sponsor_status
                    )
                    product_list_model.save()

                    # saving to Game sponsored product list
                    if sponsor_status == 'yes':
                        spnsored_prdct = ProductList.objects.get(product_id=product_id)
                        sponsord_prdct_for_game = SponsoredProductForPrize(product=spnsored_prdct)
                        sponsord_prdct_for_game.save()
                if policy == 'own':
                    product_list_model = ProductList(
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
                        sponsor_status=sponsor_status
                    )
                    product_list_model.save()

                    # saving to Game sponsored product list
                    if sponsor_status == 'yes':
                        spnsored_prdct = ProductList.objects.get(product_id=product_id)
                        sponsord_prdct_for_game = SponsoredProductForPrize(product=spnsored_prdct)
                        sponsord_prdct_for_game.save()

                messages.success(request, "Successfully added!")
                return redirect('sellerAddProduct')

        except:
            if policy == 'company':
                product_list_model = ProductList(
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
                    security_policy="apcp",
                    return_policy="apcp",
                    delivery_policy="apcp",
                    store_name=store__name,
                    store_link=store_link,
                    about_store=about_store,
                    in_stock=in_stock,
                    policy_followed=policy,
                    sponsor_status=sponsor_status
                )
                product_list_model.save()

                # saving to Game sponsored product list
                if sponsor_status == 'yes':
                    spnsored_prdct = ProductList.objects.get(product_id=product_id)
                    sponsord_prdct_for_game = SponsoredProductForPrize(product=spnsored_prdct)
                    sponsord_prdct_for_game.save()
            if policy == 'own':
                product_list_model = ProductList(
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
                    sponsor_status=sponsor_status
                )
                product_list_model.save()

                # saving to Game sponsored product list
                if sponsor_status == 'yes':
                    spnsored_prdct = ProductList.objects.get(product_id=product_id)
                    sponsord_prdct_for_game = SponsoredProductForPrize(product=spnsored_prdct)
                    sponsord_prdct_for_game.save()

            messages.success(request, "Successfully added!")
            return redirect('sellerAddProduct')

    context = {
        'product_cat': product_cat,
        'product_subcat': product_subcat,
    }

    return render(request, 'backEnd__sellerDashboard/product/add_product.html', context)

@login_required(login_url='/fe/login/register')
def seller_update_custom_product(request, pk):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

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

        curnt_product_cat = ProductCategory.objects.get(pk=category)

        curnt_product_subcat = None
        if sub_category:
            curnt_product_subcat = ProductSubCategory.objects.get(pk=sub_category)

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
                fs.delete(current_product_data.product_thumbnail.name)

                extra_imgs = request.FILES.getlist('product__extra__images')
                length_of_extra_imgs = len(extra_imgs)

                if extra_imgs:
                    if length_of_extra_imgs > 0:
                        for img in extra_imgs:
                            product_extra_img_model = ProductImg.objects.create(
                                product_id=current_product_data.product_id, product_type='mcp', img=img)
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
                    return redirect('sellerCustomProductList')

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
                    return redirect('sellerCustomProductList')
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
            if sponsor_status == 'no' and len(
                    SponsoredProductForPrize.objects.filter(product=current_product_data)) > 0:
                sponsored_product = SponsoredProductForPrize.objects.get(product=current_product_data)
                sponsored_product.delete()

            if sponsor_status == 'yes' and len(
                    SponsoredProductForPrize.objects.filter(product=current_product_data)) <= 0:
                sponsored_product = SponsoredProductForPrize(product=current_product_data)
                sponsored_product.save()

            length_of_extra_imgs = len(extra_imgs)
            if extra_imgs:
                if length_of_extra_imgs > 0:
                    for img in extra_imgs:
                        product_extra_img_model = ProductImg.objects.create(
                            product_id=current_product_data.product_id, product_type='mcp', img=img)
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
                return redirect('sellerCustomProductList')
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
                return redirect('sellerCustomProductList')

    context = {
        'current_pk': pk,
        'current_product_data': current_product_data,
        'product_category': product_category,
        'product_subcategory': product_subcat,
    }

    return render(request, 'backEnd__sellerDashboard/product/seller_update_custom_product.html', context)

@login_required(login_url='/fe/login/register')
def seller_custom_product_list(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # product list
    product_list = ProductList.objects.filter(user=request.user)

    context = {
        'product_list': product_list,
    }

    return render(request, 'backEnd__sellerDashboard/product/seller_custom_prdct_list.html', context)


@login_required(login_url='/fe/login/register')
def seller_custom_product_detail(request, pk, product_id):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # current obj
    current_product = ProductList.objects.get(pk=pk)

    context = {
        'current_pk': pk,
        'current_product': current_product,
    }

    return render(request, 'backEnd__sellerDashboard/product/product_details.html', context)

@login_required(login_url='/fe/login/register')
def seller_del_custom_product(request, pk, product_id):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    try:
        current_obj = ProductList.objects.get(pk=pk)
        fs = FileSystemStorage()
        # checking wheathe it has any extra images or not
        related_imgs_of_currnt_obj = ProductImg.objects.filter(product_id=product_id)

        if related_imgs_of_currnt_obj:
            for img in related_imgs_of_currnt_obj:
                fs.delete(img.img.name)
                img.delete()

        # deleting product thumbnail obj
        fs.delete(current_obj.product_thumbnail.name)
        current_obj.delete()
        messages.success(request, 'Successfully deleted!')
        return redirect('sellerCustomProductList')
    except:
        messages.warning(request, 'Can not be deleted! Try again!')
        return redirect('sellerCustomProductList')

    return redirect('sellerCustomProductList')


# pacages part starts********************************************
@login_required(login_url='/fe/login/register')
def seller_all_packages(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # existing package list
    package_list = PackageList.objects.all()

    context = {
        'package_list': package_list,
    }

    return render(request, 'backEnd__sellerDashboard/packages/packages.html', context)

@login_required(login_url='/fe/login/register')
def seller_payforPurchasingPackage(request, package_id):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # current package
    current_package = get_object_or_404(PackageList, package_id=package_id)

    if request.method == 'GET':
        paid_amount = request.GET.get('paid_amount')
        package_id = request.GET.get('package_id')
        order_data = request.GET.get('order_data')

        if paid_amount and package_id and order_data:
            payment_information = json.loads(order_data)
            paymentID = payment_information['id']

            # payee info
            payee_email = payment_information['purchase_units'][0]['payee']['email_address']
            payee_marchnt_id = payment_information['purchase_units'][0]['payee']['merchant_id']

            # payer info
            payer_name = payment_information['payer']['name']['given_name'] + ' ' + payment_information['payer']['name']['surname']
            payer_email = payment_information['payer']['email_address']
            payer_id = payment_information['payer']['payer_id']
            payer_post_code = payment_information['payer']['address']['postal_code']
            payer_country_code = payment_information['payer']['address']['country_code']

            package_purchased_list_model = SellerPurchasedPackages.objects.create(
                seller=request.user,
                package=current_package,
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

    context = {
        'current_package': current_package,
    }

    return render(request, 'backEnd__sellerDashboard/packages/paymentForPackage.html', context)

@login_required(login_url='/fe/login/register')
def seller_payment_success_msg(request, username):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    return render(request, 'backEnd__sellerDashboard/packages/success_msg.html')

@login_required(login_url='/fe/login/register')
def seller_package_details(request, package_id):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    current_package = get_object_or_404(PackageList, package_id=package_id)

    context = {
        'current_package': current_package,
    }

    return render(request, 'backEnd__sellerDashboard/packages/package_details.html', context)



@login_required(login_url='/fe/login/register')
def seller_collect_product(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # member current membership rank
    current_membership_rank = SellerMembershipStatus.objects.filter(user=request.user).first()

    # filter all the products which offered to everyone
    offered_products_for_current_user = OfferedSingleProductBasedOnMembershipRank.objects.filter(membership_rank=current_membership_rank.membership_rank)

    # collect categories which has at least one product
    cats_with_atLeastOne_product = []
    all_product_cats = ProductCategory.objects.all()
    for cat in all_product_cats:
        for product in offered_products_for_current_user:
            if product.product_cat.pk == cat.pk and cat not in cats_with_atLeastOne_product:
                cats_with_atLeastOne_product.append(cat)

    context = {
        'offered_products_for_current_user': offered_products_for_current_user,
        'cats_with_atLeastOne_product': cats_with_atLeastOne_product,
        'offered_products_for_current_user': offered_products_for_current_user,
    }

    return render(request, 'backEnd__sellerDashboard/product/collect_product.html', context)

@login_required(login_url='/fe/login/register')
def seller_addProductToCollections(request, product_id):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    try:
        product = ProductList.objects.filter(product_id=product_id).first()

        # user current collections
        seller_current_collections = SellerCollections.objects.filter(seller=request.user).filter(product=product)

        if seller_current_collections:
            messages.warning(request, "Already exist in your store!")
            return redirect('sellerCollectProduct')
        else:
            if product:
                seller_collections_model = SellerCollections.objects.create(
                    seller=request.user,
                    product=product
                )
                messages.success(request, "Successfully added to your store!")
                return redirect('sellerCollectProduct')
            else:
                messages.warning(request, "Can't be added to your store! Try again!")
                return redirect('sellerCollectProduct')
    except:
        messages.warning(request, "Product not found! Try again!")
        return redirect('sellerCollectProduct')

    return redirect('sellerCollectProduct')


@login_required(login_url='/fe/login/register')
def seller_productCollections(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # current seller collections
    current_collections = SellerCollections.objects.filter(seller=request.user)

    context = {
        'current_collections': current_collections,
    }

    return render(request, 'backEnd__sellerDashboard/product/collections.html', context)

@login_required(login_url='/fe/login/register')
def seller_profile_edit(request, username):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # profile pic
    profile_pic = UserProfilePicture.objects.filter(user=request.user).first()
    context = {
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd__sellerDashboard/profile/edit_profile.html', context)

@login_required(login_url='/fe/login/register')
def seller_profile_setting(request, username):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    # profile pic
    profile_pic = UserProfilePicture.objects.select_related().filter(user=request.user).first()
    context = {
        'profile_pic' : profile_pic,
    }

    return render(request, 'backEnd__sellerDashboard/profile/my_profile.html', context)


@login_required(login_url='/fe/login/register')
def seller_update_profile_pic(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        profile_picture = request.FILES['profile_pic']
        submit = request.POST.get('submit',None)


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
                if submit is not None:
                    return redirect('sellerProfileEdit', username=request.user.username)
                else:
                    return redirect('sellerProfileSetting', username=request.user.username)
            except:
                user_profile_pic = UserProfilePicture(user=request.user, pic=profile_picture)
                user_profile_pic.save()
                messages.success(request, "Successfully updated!")
                if submit is not None:
                    return redirect('sellerProfileEdit', username=request.user.username)
                else:
                    return redirect('sellerProfileSetting', username=request.user.username)

    return render(request, 'backEnd__sellerDashboard/profile/my_profile.html')


@login_required(login_url='/fe/login/register')
def seller_update_full_name(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

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
                return redirect('sellerProfileSetting', username=request.user.username)
            except:
                messages.warning(request, "Can't be updated!")
                return redirect('sellerProfileSetting', username=request.user.username)

    return render(request, 'backEnd__sellerDashboard/profile/my_profile.html')

@login_required(login_url='/fe/login/register')
def seller_update_full_name_username(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')

        if fname and lname and username:
            try:
                user = Account.objects.get(email=request.user.email)
                user.fname = fname
                user.laname = lname
                if username != request.user.username:
                    user.username = username
                user.save()
                messages.success(request, "Successfully updated!")
                return redirect('sellerProfileEdit', username=request.user.username)
            except:
                messages.warning(request, "Can't be updated!")
                return redirect('sellerProfileEdit', username=request.user.username)

    return render(request, 'backEnd__sellerDashboard/profile/my_profile.html')


@login_required(login_url='/fe/login/register')
def seller_update_user_password(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

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
                    return redirect("frontEndLoginRegister")
            except:
                messages.warning(request, "Can't be updated! Try again!")
                return redirect('sellerProfileSetting', username=request.user.username)

    return render(request, 'backEnd__sellerDashboard/profile/my_profile.html')

@login_required(login_url='/fe/login/register')
def seller_reset_user_password(request):

    if request.user.is_seller != True:
        return redirect('frontEndLoginRegister')

    if request.method == 'POST':
        confirm_pass = request.POST.get('confirm_pass')
        new_pass = request.POST.get('new_pass')

        if new_pass == confirm_pass:
            try:
                user = Account.objects.get(email=request.user.email)
                if user is not None:
                    user.set_password(new_pass)
                    user.save()
                    messages.success(request, "Successfully updated!")
                    return redirect("frontEndLoginRegister")
            except:
                messages.warning(request, "Can't be updated! Try again!")
                return redirect('sellerProfileEdit', username=request.user.username)

    return redirect('sellerProfileEdit', username=request.user.username)





