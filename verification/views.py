from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from user.models import VerificationCode, Account
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


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

    try:
        user = Account.objects.get(username=username)
        user.status = '1'
        user.is_active = True
        user.save()
    except:
        pass

    return render(request, 'verification/verify_accnt.html')
