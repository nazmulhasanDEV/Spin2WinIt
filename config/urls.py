from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('adminPanel.urls')),
    path('', include('adminPanel.conversions.urls')),
    path('', include('product.shopify.urls')),
    path('', include('sellerDashboard.urls')),
    path('product/', include('product.urls')),
    path('game/', include('game.urls')),
    path('', include('verification.urls')),
    path('', include('advertisement.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Spin & Win Adminstration"
admin.site.index_title = "Site Models"
admin.site.site_title = "Database Adminstration"


