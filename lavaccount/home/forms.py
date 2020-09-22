from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField, AuthenticationForm


class RegisterForm(forms.Form):
    """ Форма для регистрации """
    username = UsernameField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    email = forms.EmailField(
        label='Адрес электронной почты',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False
    )


class LoginForm(AuthenticationForm):
    """ Форма расширяющая форму авторизации """
    system = forms.CharField(widget=forms.HiddenInput())
    browser = forms.CharField(widget=forms.HiddenInput())


class MasterPasswordResetForm(forms.Form):
    """ Форма сброса мастер пароля """
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus': True})
    )


class EmailChangeForm(forms.Form):
    """ Форма изменения электронной почты """
    email = forms.EmailField(
        label='Адрес электронной почты',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'autofocus': True})
    )
