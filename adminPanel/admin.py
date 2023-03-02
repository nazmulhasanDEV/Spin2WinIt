from django.contrib import admin
from .conversions.models import *
from .models import *


#
# class UserTypingTestListAdmin(admin.ModelAdmin):
#     list_display = ("user", "duration", "accuracy", "wpm", "wrong_chars", "created")
# admin.site.register(UserTypingTestList, UserTypingTestListAdmin)

class ProductCategoryListAdmin(admin.ModelAdmin):
    list_display = ("name", "created")
admin.site.register(ProductCategory, ProductCategoryListAdmin)


class ProductSubCatListAdmin(admin.ModelAdmin):
    list_display = ("category", "name", "created")
admin.site.register(ProductSubCategory, ProductSubCatListAdmin)


# membership rank
admin.site.register(MemberShipRank)

# membership rank status per user
admin.site.register(SellerMembershipStatus)

# about us
admin.site.register(AboutUs)

# contact us
admin.site.register(ContactUs)

admin.site.register(SiteLogo)

# subscriber model
admin.site.register(SubscriberList)

admin.site.register(FreeDelivery)
admin.site.register(SafePayment)
admin.site.register(ShopWithConfidence)
admin.site.register(HelpCenter)
admin.site.register(CustomerMessageList)

# members and shoppers policy
admin.site.register(MembersPolicy)
admin.site.register(ShopperPolicy)

admin.site.register(VisitorInfo)
admin.site.register(TotalNumVisitor)

# policy part
admin.site.register(BetaTestTermsConditions)
admin.site.register(DeliveryPolicy)

# package name section starts************************
admin.site.register(PackageNameList)
admin.site.register(PackageOptions)


# how it works section
admin.site.register(HowSpinIt2WinWorks)

# conversion models
admin.site.register(SpinConversionRateIntoUSD)
