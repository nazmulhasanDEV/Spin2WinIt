from django.contrib import admin
from .models import *


# user prizeCart
admin.site.register(PrizeCart)
admin.site.register(CurrentDelivryRequestPrizeProduct)
admin.site.register(ProductPrizeDeliverOrder)
admin.site.register(ProductPrizeDeliverOrderPaymntHistory)

admin.site.register(SponsoredProductForPrize)
admin.site.register(GameSetting)
admin.site.register(PointAs_Prize)
admin.site.register(SegmentList)
admin.site.register(Segment)


# applicable rules/regulation for prize winner
admin.site.register(ApplicableRulesForWinner)

# total number of times played the game/spinned the wheel
admin.site.register(TotalNumOfTimesPlayed)

# terms and policies for game
admin.site.register(GameTermsPolicies)