from django.contrib import admin
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

admin.site.register(VisitorInfo)
admin.site.register(TotalNumVisitor)
