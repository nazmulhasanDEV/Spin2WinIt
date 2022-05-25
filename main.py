# user last login info
    last_logged_in = None
    if request.user.is_authenticated:
        last_logged_in = request.user.last_login + timezone.timedelta(days=1)
        timezone_now = timezone.now()

        if last_logged_in <= timezone_now:
            current_user_point_wallet = PointWallet.objects.filter(user=request.user).first()
            if current_user_point_wallet:
                current_user_point_wallet.available = int(current_user_point_wallet.available) + 50 # daily sign in bonus amount
                # current_user_point_wallet.save()
                messages.success(request, "Congratulations! You got 50 reward points as daily sign in bonus!")
                # return redirect('frontEndHome')




# give user 50 points reward as daily sign in bonus
last_logged_in = None
if request.user.is_authenticated:
    last_logged_in = request.user.last_login + timezone.timedelta(seconds=15)
    timezone_now = timezone.now()

    if GivenDailySignInBonusUsrList.objects.filter(user=request.user).count() <= 0:
        # save to daily bonus gotten user list
        daily_signin_bonusUser_list = GivenDailySignInBonusUsrList.objects.create(user=request.user)
        current_user_point_wallet = PointWallet.objects.filter(user=request.user).first()
        if current_user_point_wallet:
            current_user_point_wallet.available = int(
                current_user_point_wallet.available) + 50  # daily sign in bonus amount
            current_user_point_wallet.save()
        else:
            crnt_usr_wallet = PointWallet.objects.create(user=request.user, available=50)