from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='support_url'),
    path('protection/', views.protection, name='protection_url'),
    path('donation/', views.donation, name='donation_url'),
]
