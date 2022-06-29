from django.contrib import admin
from .models import *



# ads script settings
admin.site.register(AdsPageName)
admin.site.register(AdsRow)
admin.site.register(AdsColPerRow)

admin.site.register(BannerProdDetail)
admin.site.register(ShopPageBanner)

admin.site.register(UserProfileAds)
