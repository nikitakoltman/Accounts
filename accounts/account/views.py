from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import service
from .models import Account


def index(request):
    # Проверка авторизации пользователя
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    accounts = None
    master_password = service.get_master_password(user_name=request.user)

    try:
        accounts = Account.objects.all().filter(user_name=request.user)
    except Account.DoesNotExist:
        pass

    return render(request, 'account.html', {'accounts': accounts, 'master_password': master_password})


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
        user_name=request.user
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
    login = request.POST.get('login', None)
    new_password = request.POST.get('new_password', None)
    account_id = request.POST.get('account_id', None)

    answer = service.change_info_account(
        site=site,
        description=description,
        login=login,
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
        user_name=request.user
    )

    return service.json_response(answer)
