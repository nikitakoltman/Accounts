from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('create_account/', views.create_account),
    path('delete_account/', views.delete_account),
    path('change_info_account/', views.change_info_account),
    path('change_or_create_master_password/', views.change_or_create_master_password),
]
