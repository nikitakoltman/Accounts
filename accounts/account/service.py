import json
import logging as log
import traceback
from datetime import datetime



from django.http import HttpResponse

from .models import Account, MasterPassword


def create_account(site: str, description: str, login: str, password: str, user_name: str) -> json:
    """ Создает новый аккаунт """

    account = Account()
    account.site = site
    account.description = description
    account.login = login
    account.password = password
    account.user_name = user_name
    account.save()

    return json.dumps(
        {
            'status': 'success',
            'result': account.id,
        })


def delete_account(account_id: int) -> json:
    """ Удаляет аккаунт """

    try:
        account = Account.objects.get(pk=account_id)
        account.delete()

        return json.dumps(
            {
                'status': 'success',
            })
    except Account.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'result': 'DoesNotExist',
            })


def change_info_account(site: str, description: str, login: str, new_password: str, account_id: int) -> json:
    """ Изменяет информацию аккаунта """

    try:
        account = Account.objects.get(pk=account_id)
        account.site = site
        account.description = description
        account.login = login

        if new_password != "":
            account.password = new_password

        account.save()

        return json.dumps(
            {
                'status': 'success',
            })
    except Account.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'result': 'DoesNotExist',
            })


def change_master_password_account(sites: str, descriptions: str, logins: str, passwords: str, new_master_password, user_name: str) -> json:
    """ Изменяет мастер пароль """

    try:
        sites = json.loads(sites)
        descriptions = json.loads(descriptions)
        logins = json.loads(logins)
        passwords = json.loads(passwords)

        master_password = MasterPassword.objects.get(user_name=user_name)

        # Перезаписываем все аккаунты на новые значения
        account = Account.objects.all().filter(user_name=user_name)
        for item in account:
            item.site = sites[str(item.id)]
            item.description = descriptions[str(item.id)]
            item.login = logins[str(item.id)]
            item.password = passwords[str(item.id)]
            item.save()
    # Если в базе нет мастер пароля то создаем его
    except MasterPassword.DoesNotExist:
        master_password = MasterPassword()
        master_password.user_name = user_name

    master_password.value = new_master_password
    master_password.save()

    return json.dumps(
        {
            'status': 'success',
        })


def get_master_password_account(user_name: str) -> json:
    """ Возвращает мастер пароль """

    try:
        master_password = MasterPassword.objects.get(user_name=user_name)
        return json.dumps(
            {
                'status': 'success',
                'result': master_password.value,
            })
    except MasterPassword.DoesNotExist:
        return json.dumps(
            {
                'status': 'error',
                'result': 'DoesNotExist',
            })


def catching_exceptions(function):
    """ Декоратор для отлова не предвиденных исключений, а также проверка ajax """

    def wrapper(request):
        # Если запрос был не ajax, а например по прямой ссылке...
        if not request.is_ajax():
            return HttpResponse(status=404)

        try:
            return function(request)
        except Exception as err:
            # Логирование исключений в консоль
            log.error(traceback.format_exc())

            # Запись исключений в файл
            with open('../log.txt', 'a') as f:
                f.write(f'ERROR | {datetime.now().strftime("%d.%m.%Y %H:%M:%S")} | {traceback.format_exc()} \n\n')

            return HttpResponse(
                    json.dumps(
                        {
                            'status': 'error',
                            'result': str(err),
                        }))
    return wrapper
