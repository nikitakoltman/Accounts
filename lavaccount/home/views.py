import re
import base64

from api import service
from api.models import Account, TokenConfirmEmail, MasterPassword

from django.views.generic import TemplateView

from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import RegisterForm, ConfirmEmailForm, MasterPasswordResetForm

from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text

from api.tokens import account_activation_token

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html')

    context = {
        'accounts': Account.objects.filter(user=request.user),
        'master_password': service.get_master_password(user=request.user)
    }

    return render(request, 'home.html', context)


def noscript(request):
    return render(request, 'noscript.html')


def lk(request):
    context = {
        'title': 'Личный кабинет'
    }
    return render(request, 'lk.html', context)


def confirm_email_done(request):
    context = {
        'title': 'Письмо отправленно'
    }
    return render(request, 'email/confirm_email_done.html', context)


def confirm_email_complete(request):
    valid = False

    if 'valid' in request.session:
        valid = request.session['valid']
        del request.session['valid']

    context = {
        'title': 'Подтверждение почты',
        'valid': valid
    }
    return render(request, 'email/confirm_email_complete.html', context)


# TODO: Удалить
def email(request):
    return render(request, 'email/page_to_confirm_email.html', {'username':request.user.username, 'token': service.generate_token()})


def confirm_email(request):
    if not request.user.is_authenticated:
        return redirect(reverse("home_url"))
    service.confirm_email(request.user, request.user.email)
    return redirect(reverse("confirm_email_done_url"))


def activate_email(request, uidb64, token):
    if not request.user.is_authenticated:
        return redirect(reverse("home_url"))

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.profile.is_active_email = True
        user.save()
        request.session['valid'] = True
    return redirect(reverse("confirm_email_complete_url"))


def master_password_reset(request):
    if not request.user.is_authenticated:
        return redirect(reverse("home_url"))

    try:
        context = {
            'title': 'Сброс мастер пароля',
            'form': MasterPasswordResetForm,
            'form_error': None
        }

        if request.method == 'POST':
            password = request.POST.get('password')

            if check_password(password, request.user.password):
                master_password = MasterPassword.objects.get(user=request.user)
                master_password.delete()

                accounts = Account.objects.filter(user=request.user)
                accounts.delete()

                return redirect(reverse("home_url"))
            else:
                context.update({
                    'form_error': 'Password is not valid'
                })
    except Exception as err:
        context.update({
            'form_error': err
        })
    return render(request, 'registration/master_password_reset.html', context)


@service.base_view
def create_account(request):
    """ Создает аккаунт """
    site = request.POST.get('site', None)
    description = request.POST.get('description', None)
    login = request.POST.get('login', None)
    password = request.POST.get('password', None)

    answer = service.create_account(
        site=site,
        description=description,
        login=login,
        password=password,
        user=request.user
    )

    return service.json_response(answer)


@service.base_view
def delete_account(request):
    """ Удаляет аккаунт """
    account_id = request.POST.get('account_id', None)
    answer = service.delete_account(account_id)
    return service.json_response(answer)


@service.base_view
def change_info_account(request):
    """ Изменяет информацию об аккаунте """
    site = request.POST.get('site', None)
    description = request.POST.get('description', None)
    new_login = request.POST.get('new_login', None)
    new_password = request.POST.get('new_password', None)
    account_id = request.POST.get('account_id', None)

    answer = service.change_info_account(
        site=site,
        description=description,
        new_login=new_login,
        new_password=new_password,
        account_id=account_id
    )

    return service.json_response(answer)


@service.base_view
def change_or_create_master_password(request):
    """ Изменяет мастер пароль """
    sites = request.POST.get('sites', None)
    descriptions = request.POST.get('descriptions', None)
    logins = request.POST.get('logins', None)
    passwords = request.POST.get('passwords', None)
    new_master_password = request.POST.get('new_master_password', None)

    answer = service.change_or_create_master_password(
        sites=sites,
        descriptions=descriptions,
        logins=logins,
        passwords=passwords,
        new_master_password=new_master_password,
        user=request.user
    )

    return service.json_response(answer)


@service.base_view
def check_username_and_email(request):
    """ Проверяет существование имени и почты в БД """
    username = request.POST.get('username', None)
    email = request.POST.get('email', None)

    answer = service.check_username_and_email(
        username=username,
        email=email
    )

    return service.json_response(answer)


def lav_login(request):
    """ Авторизация пользователей """
    if request.user.is_authenticated:
        return redirect(reverse("home_url"))

    context = {
        'form': AuthenticationForm,
        'form_error': None
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("home_url"))
        else:
            context.update({
                'form_error': 'Login error'
            })
    return render(request, 'registration/login.html', context)


class RegisterView(TemplateView):
    """ Регистрация пользователей """
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("home_url"))

        context = {
                'form': RegisterForm,
                'form_error': None
            }

        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            answer = self.check_if_password_correct(password, password2)
            if answer == 'success':
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )

                    service.confirm_email(user, email)

                    return redirect(reverse("lav_login"))
                except Exception as err:
                    context.update({
                        'form_error': err,
                        'username': username,
                        'email': email
                    })
            else:
                context.update({
                        'form_error': answer,
                        'username': username,
                        'email': email
                    })
        return render(request, self.template_name, context)


    def check_if_password_correct(self, password: str, password2: str) -> str:
        """ Проверка корректности пароля """
        if password != password2:
            return 'broken rule [pass == pass2]'
        if len(password) < 8:
            return 'broken rule [len > 8]'
        elif re.search('[a-z]', password) is None:
            return 'broken rule [a-z]'
        elif re.search('[A-Z]', password) is None:
            return 'broken rule [A-Z]'
        elif re.search('[0-9]', password) is None:
            return 'broken rule [0-9]'
        else:
            return 'success'
