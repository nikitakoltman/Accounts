import re

from api import service
from api.models import Account

from django.views.generic import TemplateView

from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import RegisterForm


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html')

    context = {
        'accounts': Account.objects.filter(user=request.user),
        'master_password': service.get_master_password(user=request.user)
    }

    return render(request, 'account.html', context)


def noscript(request):
    return render(request, 'noscript.html')


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


class RegisterView(TemplateView):
    """ Регистрация пользователей """
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        context = {
                'form': RegisterForm,
                'form_error': None
            }

        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if self.check_if_password_correct(password, password2):
                try:
                    User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    return redirect(reverse("login_url"))
                except Exception as err:
                    context.update({
                        'form_error': err,
                        'username': username,
                        'email': email
                    })

        return render(request, self.template_name, context)

    def check_if_password_correct(self, password: str, password2: str) -> bool:
        """ Проверка корректности пароля """
        if password == password2:
            pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
            return bool(pattern_password.match(password))
        else:
            return False