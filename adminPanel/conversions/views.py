import datetime
from django.shortcuts import render, redirect, get_object_or_404
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
from django.db.models import Q, Prefetch
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
from core.models import *
from config.activate_deactivate_status import activate_status, deactivate_status
from config.custom_functions import delete_obj
from django.db.models import Avg, Sum, Count, Max

# woocomerce to connect with woocommerce store
from woocommerce import API
import asyncio
import requests


@login_required(login_url='/ap/register/updated')
def updateSpinRate(request):

    if request.method == 'POST':
        rate = request.POST['spin_value_in_usd']

        try:
            if rate and len(SpinConversionRateIntoUSD.objects.all()) <= 0:
                storeDB = SpinConversionRateIntoUSD.objects.create(spinRateValueInUSD=rate)
                messages.success(request, "Spin conversion rate updated successfully!")
                return redirect('updateSpinRate')
            else:
                storeDB = SpinConversionRateIntoUSD.objects.filter().first()
                storeDB.spinRateValueInUSD = rate
                storeDB.save()
                messages.success(request, "Spin conversion rate updated successfully!")
                return redirect('updateSpinRate')
        except:
            messages.warning(request, "Something went wrong. Try again!")
            return redirect('updateSpinRate')


    return render(request, 'backEnd_superAdmin/settings/settings.html')