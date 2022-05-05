from django.contrib import admin
from .models import *

admin.site.register(SponsoredProductForPrize)
admin.site.register(GameSetting)
admin.site.register(PointAs_Prize)
admin.site.register(SegmentList)
admin.site.register(Segment)


# applicable rules/regulation for prize winner
admin.site.register(ApplicableRulesForWinner)