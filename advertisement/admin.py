from django.contrib import admin
from .models import *



# ads script settings
class AdsScriptPageListAdmin(admin.ModelAdmin):
    list_display = ('page_id', 'name',)
    list_filter = ('page_id', 'name',)
    list_display_links = ('page_id', 'name',)

admin.site.register(AdsPageName, AdsScriptPageListAdmin)


class AdsScriptRowListAdmin(admin.ModelAdmin):
    list_display = ('row_id', 'page_name', 'name',)
    list_filter = ('row_id', 'page_name', 'name',)
    list_display_links = ('row_id', 'page_name', 'name',)
admin.site.register(AdsRow, AdsScriptRowListAdmin)

class AdsScriptColListAdmin(admin.ModelAdmin):
    list_display = ('col_id', 'row', 'col_name',)
    list_filter = ('col_id', 'row', 'col_name',)
    list_display_links = ('col_id', 'row', 'col_name',)

admin.site.register(AdsColPerRow, AdsScriptColListAdmin)

admin.site.register(BannerProdDetail)
admin.site.register(ShopPageBanner)

admin.site.register(UserProfileAds)

class AdsScriptListAdmin(admin.ModelAdmin):
    list_display = ('page', 'row', 'col', 'adsScript')
    list_filter = ('page', 'row', 'col', 'adsScript')

admin.site.register(AdsScript, AdsScriptListAdmin)
