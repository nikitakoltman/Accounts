import functools
import json
import threading
import logging as log
import traceback
from datetime import datetime

from accounts.settings import DEBUG
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, JsonResponse

from .models import Account, MasterPassword
from django.core.mail import EmailMessage
from django.template.loader import get_template
from configs.config import EMAIL_HOST_USER


class EmailThread(threading.Thread):
    """ Отправка почты в новом потоке """
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


def send_email(email: str, subject: str, template: str, context: str) -> None:
    """ Отправка почты """
    htmly = get_template(f'email/{template}.html')
    html_content = htmly.render(context)

    EmailThread(subject, html_content, [email]).start()


def confirm_email(username: str, email: str) -> None:
    send_email(
        email=email,
        subject='Добро пожаловать в LavAccount',
        template='confirm_email',
        context= {
            'username': username
        }
    )


def create_account(site: str, description: str, login: str, password: str, user: User) -> dict:
    """ Создает новый аккаунт """
    account = Account.objects.create(
        user=user,
        site=site,
        description=description,
        login=login,
        password=password
    )

    return {
        'status': 'success',
        'account_id': account.id
    }


def delete_account(account_id: int) -> dict:
    """ Удаляет аккаунт """
    try:
        account = Account.objects.get(id=account_id)
        account.delete()

        return {
            'status': 'success'
        }
    except Account.DoesNotExist:
        return {
            'status': 'error',
            'result': 'DoesNotExist'
        }


def change_info_account(site: str, description: str, new_login: str, new_password: str, account_id: int) -> dict:
    """ Изменяет информацию аккаунта """
    try:
        account = Account.objects.get(id=account_id)
        account.site = site
        account.description = description

        if new_login is None:
            account.login = account.login
        else:
            account.login = new_login

        if new_password is None:
            account.password = account.password
        else:
            account.password = new_password

        account.save()

        return {
            'status': 'success'
        }
    except Account.DoesNotExist:
        return {
            'status': 'error',
            'result': 'DoesNotExist'
        }


def change_or_create_master_password(sites: str, descriptions: str, logins: str, passwords: str,
                                     new_master_password: str, user: User) -> dict:
    """ Изменяет мастер пароль """
    master_password, is_created = MasterPassword.objects.get_or_create(
        user=user,
        defaults={
            'password': new_master_password
        }
    )

    # Если False значит объект найден, и не был создан, а это значит, что
    # существуют записанные аккаунты и их можно переписывать
    if not is_created:
        sites = json.loads(sites)
        descriptions = json.loads(descriptions)
        logins = json.loads(logins)
        passwords = json.loads(passwords)

        # Перезаписываем все аккаунты на новые значения
        account = Account.objects.filter(user=user)

        for item in account:
            item.site = sites[str(item.id)]
            item.description = descriptions[str(item.id)]
            item.login = logins[str(item.id)]
            item.password = passwords[str(item.id)]
            item.save()

        master_password.password = new_master_password
        master_password.save()

    return {
        'status': 'success'
    }


def check_username_and_email(username: str, email: str) -> dict:
    """ Проверяет существование имени и почты в БД """
    is_exist_username = False
    is_exist_email = False

    try:
        user = User.objects.get(username=username)
        is_exist_username = True
    except User.DoesNotExist:
        pass

    try:
        user = User.objects.get(email=email)
        is_exist_email = True
    except User.DoesNotExist:
        pass

    return {
        'status': 'success',
        'is_exist_username': is_exist_username,
        'is_exist_email': is_exist_email
    }


def get_master_password(user: User) -> str:
    """ Возвращает мастер пароль """
    try:
        master_password = MasterPassword.objects.get(user=user)
        return master_password.password
    except MasterPassword.DoesNotExist:
        return 'DoesNotExist'


def base_view(function):
    """ Декоратор для вьюшек, проверяет ajax и обрабатывает исключения """

    @functools.wraps(function)
    def wrapper(request):
        # Если запрос был не ajax, а например по прямой ссылке...
        if not request.is_ajax():
            return HttpResponse(status=404)

        try:
            with transaction.atomic():
                return function(request)
        except Exception as err:
            if DEBUG:
                log.error(traceback.format_exc())
                error_response(err)
            else:
                write_error_to_log_file(traceback.format_exc())

    return wrapper


def json_response(data: dict, status=200) -> JsonResponse:
    """ Возвращает JSON с правильными HTTP заголовками и в читаемом
    в браузере виде в случае с кириллицей """
    return JsonResponse(
        data=data,
        status=status,
        safe=not isinstance(data, list),
        json_dumps_params={
            'ensure_ascii': False
        }
    )


def error_response(exception: Exception) -> json_response:
    """ Форматирует HTTP ответ с описанием ошибки """
    result = {
        'status': 'error',
        'result': str(exception),
    }

    return json_response(data=result, status=400)


def write_error_to_log_file(traceback_format_exc: str) -> None:
    """ Запись исключения в файл """
    with open('../log.txt', 'a') as f:
        f.write(
            f'ERROR | {datetime.now().strftime("%d.%m.%Y %H:%M:%S")} | {traceback_format_exc} \n\n'
        )
