from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home_url'),
    path('noscript/', views.noscript, name='noscript_url'),
    path('register/', views.RegisterView.as_view(), name="register_url"),
    path('create_account/', views.create_account),
    path('delete_account/', views.delete_account),
    path('change_info_account/', views.change_info_account),
    path('change_or_create_master_password/', views.change_or_create_master_password),

    path('register/check_username_and_email/', views.check_username_and_email),
    path('confirm_email/', views.confirm_email, name='confirm_email_url'),

    path('reset-account/', views.reset_account, name='reset_account_url'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('email/', views.email, name='email_url'), # TODO: удалить
]
