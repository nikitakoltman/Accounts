from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home_url'),
    path('noscript', views.noscript, name='noscript_url'),
    path('register/', views.RegisterView.as_view(), name="register_url"),
    path('create_account/', views.create_account),
    path('delete_account/', views.delete_account),
    path('change_info_account/', views.change_info_account),
    path('change_or_create_master_password/', views.change_or_create_master_password),
]
