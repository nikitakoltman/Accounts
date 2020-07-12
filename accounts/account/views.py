import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Account
from .service import AccountManage, catching_exceptions


def index(request):
    """ Главная страница сайта """

    # Проверка авторизации пользователя
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    accounts = None

    try:
        accounts = Account.objects.all().filter(user=request.user)
    except Account.DoesNotExist:
        pass

    return render(request, 'account.html', {'accounts': accounts})


@catching_exceptions
def create_account(request):
    """ Создает аккаунт """

    site = request.POST.get('site', None)
    description = request.POST.get('description', None)
    login = request.POST.get('login', None)
    password = request.POST.get('password', None)

    answer = AccountManage.create(
        site, description, login, password, request.user)

    return HttpResponse(answer)


@catching_exceptions
def delete_account(request):
    """ Удаляет аккаунт """

    id = request.POST.get('datadissid', None)
    answer = AccountManage.delete(id)
    return HttpResponse(answer)


@catching_exceptions
def change_info_account(request):
    """ Изменяет информацию об аккаунте """

    id = request.POST.get('id', None)
    site = request.POST.get('site', None)
    description = request.POST.get('description', None)
    login = request.POST.get('login', None)
    newpassword = request.POST.get('newpassword', None)

    answer = AccountManage.change_info(
        id, site, description, login, newpassword)
    return HttpResponse(answer)


@catching_exceptions
def change_master_password_accounts(request):
    """ Изменяет мастер пароль """

    newmp = request.POST.get('newmp', None)
    sites = json.loads(request.POST.get('sites', None))
    descriptions = json.loads(request.POST.get('descriptions', None))
    logins = json.loads(request.POST.get('logins', None))
    passwords = json.loads(request.POST.get('passwords', None))

    answer = AccountManage.change_master_password(
        newmp, sites, descriptions, logins, passwords, request.user)
    return HttpResponse(answer)


@csrf_exempt
@catching_exceptions
def get_master_password_accounts(request):
    """ Возвращает мастер пароль """

    answer = AccountManage.get_master_password(request.user)
    return HttpResponse(answer)
