from django.contrib import admin
from .models import *

admin.site.register(PointWallet)
admin.site.register(ReferalBonusList)
admin.site.register(GivenDailySignInBonusUsrList)
admin.site.register(BonusPoinForRegistration)
admin.site.register(EmailInvitationBonusUserList)

admin.site.register(CreditWallet)
admin.site.register(CreditPurchasingHistory)

admin.site.register(WinningChance)
admin.site.register(WinningChancePurchasingHistory)
admin.site.register(PrizeList)
admin.site.register(PackageList)






