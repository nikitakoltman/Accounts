from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home_url'),
    path('noscript/', views.noscript, name='noscript_url'),
    path('reset-password/', views.reset_password, name='reset_password_url'),
    path('reset-account/', views.reset_account, name='reset_account_url'),
    path('register/', views.RegisterView.as_view(), name="register_url"),
    path('create_account/', views.create_account),
    path('delete_account/', views.delete_account),
    path('change_info_account/', views.change_info_account),
    path('change_or_create_master_password/', views.change_or_create_master_password),
    path('register/check_username_and_email/', views.check_username_and_email),
]
