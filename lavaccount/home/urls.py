from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.index, name='home_url'),
    path('lk/', views.lk, name='lk_url'),
    path('noscript/', views.noscript, name='noscript_url'),
    path('login/', views.lav_login, name="lav_login"),
    path('register/', views.RegisterView.as_view(), name="register_url"),

    path('create_account/', views.create_account),
    path('delete_account/', views.delete_account),
    path('change_info_account/', views.change_info_account),
    path('change_or_create_master_password/', views.change_or_create_master_password),

    path('register/check_username_and_email/', views.check_username_and_email),
    path('confirm_email/', views.confirm_email, name='confirm_email_url'),
    path('confirm_email_done/', views.confirm_email_done, name='confirm_email_done_url'),
    path('confirm_email_complete/', views.confirm_email_complete, name='confirm_email_complete_url'),
    path('activate_email/<uidb64>[0-9A-Za-z_\-]+)/<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate_email, name='activate_email'),

    path('master_password_reset/', views.master_password_reset, name='master_password_reset_url'),

    path('email/', views.email, name='email_url'), # TODO: удалить
]
