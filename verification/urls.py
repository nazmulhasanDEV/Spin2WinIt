from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^verify/user/account/$', views.verifyUserAccount, name="verifyUserAccount"),
    re_path(r'^resend/verification/code/$', views.resendVerificationCode, name="resendVerificationCode"),

    re_path(r'^user/account/veirfication/(?P<username>\w+)/(?P<phone_no>\w+)/$', views.verifyUserAccnt, name="veirfyUserAccnt"),
]
