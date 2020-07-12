import json
import logging as log
import traceback
from datetime import datetime

from django.http import HttpResponse

from .models import Account, MasterPassword


class AccountManage():
    """ Управление аккаунтами """

    @staticmethod
    def create(site, description, login, password, user):
        """ Создает новый аккаунт """

        account = Account()
        account.site = site
        account.description = description
        account.login = login
        account.password = password
        account.user = user
        account.save()

        return json.dumps(
            {
                'status': 'success',
                'result': account.id,
            })

    @staticmethod
    def delete(id):
        """ Удаляет аккаунт """

        try:
            account = Account.objects.get(id=id)
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

    @staticmethod
    def change_info(id, site, description, login, newpassword):
        """ Изменяет информацию аккаунта """

        try:
            account = Account.objects.get(id=id)
            account.site = site
            account.description = description
            account.login = login

            if newpassword != "":
                account.password = newpassword

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

    @staticmethod
    def change_master_password(newmp, sites, descriptions, logins, passwords, user):
        """ Изменяет мастер пароль """

        try:
            master_password = MasterPassword.objects.get(user=user)

            # Перезаписываем все аккаунты на новые значения
            account = Account.objects.all().filter(user=user)
            for item in account:
                item.site = sites[str(item.id)]
                item.description = descriptions[str(item.id)]
                item.login = logins[str(item.id)]
                item.password = passwords[str(item.id)]
                item.save()
        # Если в базе нет мастер пароля то создаем его
        except MasterPassword.DoesNotExist:
            master_password = MasterPassword()
            master_password.user = user

        master_password.value = newmp
        master_password.save()

        return json.dumps(
            {
                'status': 'success',
            })

    @staticmethod
    def get_master_password(user):
        """ Возвращает мастер пароль """

        try:
            master_password = MasterPassword.objects.get(user=user)
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
                f.write('ERROR | {0} | {1} \n\n'.format(datetime.now().strftime("%d.%m.%Y %H:%M:%S"), traceback.format_exc()))

            return HttpResponse(
                json.dumps(
                    {
                        'status': 'error',
                        'result': str(err),
                    }))
    return wrapper
