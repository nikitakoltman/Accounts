from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('createaccount/', views.create_account),
    path('deleteaccount/', views.delete_account),
    path('changeinfoaccount/', views.change_info_account),
    path('changemasterpassword/', views.change_master_password_accounts),
    path('getmasterpassword/', views.get_master_password_accounts),
]
