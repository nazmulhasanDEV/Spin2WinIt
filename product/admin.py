from django.contrib import admin
from .models import *

# class ProductListAdmin(admin.ModelAdmin):
#     list_display = ('user', 'category', 'title', 'new_price', 'created')
#     list_filter = ('user', 'category',)
# admin.site.register(Product_list, ProductListAdmin)

class Product_ListAdmin(admin.ModelAdmin):
    list_display = ('user','product_type', 'category', 'title', 'new_price', 'created')
    list_filter = ('user', 'category',)
admin.site.register(ProductList, Product_ListAdmin)

admin.site.register(ProductImg)


admin.site.register(ProductDiscount)
admin.site.register(ProductRating)

admin.site.register(WoocommerceProductList)

# admin.site.register(AllProductList)


# home page sliders
admin.site.register(BannerList)
admin.site.register(HomeMiniTopBanner)
admin.site.register(HomeMiniBottomBanner)

# cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user', 'product', 'quantity')
    list_display_links = ('user', 'product')
admin.site.register(Cart, CartAdmin)


# cart
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter = ('user', 'product')
    list_display_links = ('user', 'product')
admin.site.register(WishList, WishListAdmin)

# order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'order_status', 'delivery_status')
    list_filter = ('user', 'order_status', 'delivery_status')

admin.site.register(OrderList, OrderAdmin)
admin.site.register(OrderedItem)

# coupon code
class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon_code', 'discount_amnt')
    list_filter = ('coupon_code', 'discount_amnt',)
    list_display_links = ( 'coupon_code', 'discount_amnt',)
admin.site.register(CouponCode, CouponCodeAdmin)

admin.site.register(AppliedCouponHistory)

# offered single products
admin.site.register(OfferedProductItemsByMembershipRank)
admin.site.register(OfferedSingleProductBasedOnMembershipRank)

