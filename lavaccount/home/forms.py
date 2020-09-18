from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'ivan123'}))
    email = forms.CharField(label='Почта', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'ivan123@mail.ru'}))
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', max_length=100, widget=forms.PasswordInput)


class MasterPasswordResetForm(forms.Form):
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput)


class ConfirmEmailForm(forms.Form):
    token = forms.CharField(label='Код подтверждения', max_length=100)
