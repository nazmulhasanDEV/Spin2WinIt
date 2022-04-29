from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from user.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from adminPanel.models import *
from core.models import *


@csrf_protect
def verifyUserAccount(request):

    if request.method == 'POST':
        code = request.POST['verification_code']

        if code:
            try:
                if request.session['v_email'] and request.session['v_code']:
                    user_email = request.session['v_email']
                    sent_code = request.session['v_code']
                    request.session.clear_expired()

                    try:
                        user = Account.objects.get(email=user_email)
                        user_in_verification_model = VerificationCode.objects.filter(user_email=user_email).first()
                        time_now = timezone.now().timestamp()
                        obj = user_in_verification_model.created.timestamp()
                        duration = time_now - obj
                        if duration >= 300:
                            return redirect('resendVerificationCode')
                        else:
                            if user and user_in_verification_model and user_in_verification_model.code == sent_code:
                                for x in VerificationCode.objects.filter(user_email=user_email).exclude(pk=user_in_verification_model.pk):
                                    x.delete()
                                user.status = '1'
                                user.is_active = True
                                user.save()
                                # deleting verification code after verification
                                user_in_verification_model.delete()

                                if user.is_seller == True or user.is_buyer == True:
                                    messages.success(request, "Your account has been verified!")
                                    return redirect('frontEndLoginRegister')

                                messages.success(request, "Your account has been verified!")
                                return redirect('apLoginSuperUser')
                    except:
                        messages.success(request, "User not found! Click to resend code!")
                        return redirect('verifyUserAccount')

            except:
                messages.success(request, "Code didn't match! Click to resend code!")
                return redirect('verifyUserAccount')


    return render(request, 'verification/verification.html')

def resendVerificationCode(request):

    return render(request, 'verification/resend_verification_code.html')



def verifyUserAccnt(request, username, phone_no):

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

    try:
        user = Account.objects.get(username=username)
        user.status = '1'
        user.is_active = True
        user.save()

        # adding 1000 points as bonus to wallet
        point_wallet = PointWallet.objects.create(user=user)
        point_wallet.available = int(point_wallet.available) + 1000
        point_wallet.save()
    except:
        pass

    context = {
        'site_logo': site_logo,
        'contact_info': contact_info,
        'free_delivery_content_setting': free_delivery_content_setting,
        'safe_payment_content_setting': safe_payment_content_setting,
        'shop_with_confidencce_content_setting': shop_with_confidencce_content_setting,
        'help_center_content_setting': help_center_content_setting,
    }

    return render(request, 'verification/verify_accnt.html', context)
