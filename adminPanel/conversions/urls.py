from django.urls import include, re_path, path
from . import views



urlpatterns = [
    re_path(r'^ap/update-spin-rate/$', views.updateSpinRate, name='updateSpinRate'),
]