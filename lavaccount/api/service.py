import functools
import hashlib
import json
import os
import re
import threading
import traceback
import urllib.request
import zipfile
from datetime import datetime

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from lavaccount.settings import (BASE_DIR, DEBUG,
                                 DONATION_NOTIFICATION_SECRET_KEY,
                                 IPINFO_IO_TOKEN, SITE_PROTOCOL,
                                 STATIC_VERSION, SUPPORT_EMAIL)
from loguru import logger as log

from .models import (Account, Donation, LoginHistory, MasterPassword,
                     SiteSetting)
from .tokens import account_activation_token


class EmailThread(threading.Thread):
    """ Отправка почты в новом потоке """

    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, os.getenv("EMAIL_HOST_USER"), self.recipient_list)
        msg.content_subtype = "html"
        msg.send()


class NewLoginHistory(threading.Thread):
    """ Создает новую запись истории авторизаций в новом потоке """

    def __init__(self, user, META, system, browser):
        self.user = user
        self.meta = META
        self.system = system
        self.browser = browser
        threading.Thread.__init__(self)

    def run(self):
        ip_system = SiteSetting.objects.get(name='get_ip_info_system').value
        client_ip = get_client_ip(self.meta)
        ip_info = get_ip_info(client_ip, ip_system)

        if ip_system == 'ipwhois.io' and ip_info['completed_requests'] == 9500:
            to_email = ''
            try:
                to_email = User.objects.get(username='admin').email
            except User.DoesNotExist:
                to_email = SUPPORT_EMAIL

            current_site = Site.objects.get_current()
            send_email(
                email=to_email,
                subject='Переполнение запросов ipwhois.io',
                template='notification_ip_info_completed_requests_to_admin',
                context={
                    'username': self.user.username,
                    'protocol': SITE_PROTOCOL,
                    'domain': current_site.domain,
                }
            )

        if ip_system == 'ipwhois.io':
            if ip_info['success']:
                if ip_info['city'] == ip_info['country']:
                    location = ip_info['country']
                else:
                    location = f"{ip_info['city']}, {ip_info['country']}"
                self.create_login_history(client_ip, location)
            else:
                write_error_to_log_file(
                    'NewLoginHistory ipwhois.io ERROR',
                    self.user.username,
                    ip_info
                )
        elif ip_system == 'ipinfo.io':
            try:
                location = f"{ip_info['city']}, {ip_info['region']}"
                self.create_login_history(client_ip, location)
            except KeyError:
                write_error_to_log_file(
                    'NewLoginHistory ipinfo.io ERROR',
                    self.user.username,
                    ip_info
                )

    def create_login_history(self, client_ip, location):
        """ Создает запись истории авторизации """
        if location is None:
            location = 'Не определено'

        LoginHistory.objects.create(
            user=self.user,
            ip=client_ip,
            system=self.system,
            location=location,
            browser=self.browser
        )

        # Удаляем последний элемент, если их становится больше 6, так как
        # в выводится 6 элементов, чтобы не мусорить в БД
        login_history = LoginHistory.objects.filter(user=self.user)
        if login_history.count() > 6:
            last_element = login_history.order_by('-id').last()
            last_element.delete()


def send_email(email: str, subject: str, template: str, context: str) -> None:
    """ Отправка почты """
    htmly = get_template(f'{template}')
    html_content = htmly.render(context)

    #EmailThread(subject, html_content, [email]).start()
    log.info('send')
    email_thread = EmailThread(subject, html_content, [email])
    email_thread.start()
    email_thread.join()


def confirm_email(user: User, email: str, subject: str, template: str) -> None:
    """ Отправить письмо о подтверждении почты """
    current_site = Site.objects.get_current()

    send_email(
        email=email,
        subject=subject,
        template=template,
        context={
            'username': user.username,
            'protocol': SITE_PROTOCOL,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
    )


def activate_email(uidb64, token) -> bool:
    """ Активация почты """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        old_users = User.objects.filter(email=user.email)
        for old_user in old_users:
            if not old_user.username == user.username:
                old_user.email = ''
                old_user.profile.is_active_email = False
                old_user.save()
        user.profile.is_active_email = True
        user.save()
        return True
    return False


def hiding_email(email: str) -> str:
    """ Скрывает тремя звездочками часть email адреса """
    try:
        return email[0:2] + '***' + email[email.index('@'):]
    except Exception:
        return ''


def calculate_hash(data: dict) -> str:
    """ Вычисляет хеш для проверки платежа """
    text = '{0}&{1}&{2}&{3}&{4}&{5}&{6}&{7}&{8}'.format(
        data.get('notification_type', ''),
        data.get('operation_id', ''),
        data.get('amount', ''),
        data.get('currency', ''),
        data.get('datetime', ''),
        data.get('sender', ''),
        data.get('codepro', ''),
        DONATION_NOTIFICATION_SECRET_KEY,
        data.get('label', '')
    )

    hash_object = hashlib.sha1(text.encode('utf-8'))
    hexd = hash_object.hexdigest()
    return hexd


def create_donation(info: dict) -> bool:
    """ Создает пожертвование """
    donate_hash = calculate_hash(info)

    if donate_hash == info.get('sha1_hash', ''):
        try:
            Donation.objects.create(
                user=User.objects.get(id=info.get('label', '')),
                data=json.dumps(info)
            )
            return True
        except ValueError:
            return False
    return False


def master_password_reset(user: User, password: str) -> bool:
    """ Сброс мастер пароля """
    if check_password(password, user.password):
        master_password = MasterPassword.objects.get(user=user)
        master_password.delete()
        accounts = Account.objects.filter(user=user)
        accounts.delete()
        return True
    return False


def get_ip_info(client_ip: str, system: str) -> dict:
    """ Получить информацию о пользователе по ip через API """
    if system == 'ipwhois.io':
        objects = 'success,message,type,country,city,completed_requests'
        url = f'https://ipwhois.app/json/{client_ip}?objects={objects}&lang=ru'
    elif system == 'ipinfo.io':
        url = f'https://ipinfo.io/{client_ip}?token={IPINFO_IO_TOKEN}'

    with urllib.request.urlopen(url) as response:
        return json.load(response)


def get_client_ip(meta) -> str:
    """ Получить ip адрес пользователя """
    x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return meta.get('REMOTE_ADDR')


def get_logs() -> list:
    """ Возвращает логи """
    logs = read_log_file(BASE_DIR + '/logs/log.json')
    return sorted_logs(logs)


def read_log_file(path: str) -> json:
    """ Читает файл с логами и возвращает json """
    with open(path) as f:
        return json.loads(f.read())


def sorted_logs(logs: json) -> list:
    """ Сортировка логов по дате, чем раньше тем выше """
    return sorted(logs.items(), key=lambda kv: kv[1]['date'], reverse=True)


def get_ip_info_system_switch(system_name: str) -> dict:
    """ Изменяет систему получения информации по ip """
    # ipwhois.io ipinfo.io
    try:
        setting = SiteSetting.objects.get(name='get_ip_info_system')
        setting.value = system_name
        setting.save()

        return {
            'status': 'success',
            'value': setting.value
        }
    except SiteSetting.DoesNotExist:
        return {
            'status': 'error',
            'result': 'doesnotexist'
        }


def site_in_service_switch(checked: str) -> dict:
    """ Изменяет состояние сайта ('true' - Закрыт / 'false' - Открыт) """
    try:
        setting = SiteSetting.objects.get(name='site_in_service')
        if checked == 'true':
            setting.value = 'true'
        else:
            setting.value = 'false'

        setting.save()

        return {
            'status': 'success',
            'checked': setting.value
        }
    except SiteSetting.DoesNotExist:
        return {
            'status': 'error',
            'result': 'doesnotexist'
        }


def create_account(site: str, description: str,
                    login: str, password: str, user: User) -> dict:
    """ Создает новый аккаунт """
    if Account.objects.count() >= 200:
        return {
            'status': 'error',
            'message': 'accountlimitreached'
        }

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
            'result': 'doesnotexist'
        }


def change_info_account(site: str, description: str, new_login: str,
                        new_password: str,account_id: int) -> dict:
    """ Изменяет информацию аккаунта """
    try:
        account = Account.objects.get(id=account_id)
        account.site = site
        account.description = description

        if new_login == '':
            account.login = account.login
        else:
            account.login = new_login

        if new_password == '':
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
            'result': 'doesnotexist'
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


def check_username(username: str) -> dict:
    """ Проверяет существование имени в БД """
    is_exist_username = False

    if User.objects.filter(username=username).exists():
        is_exist_username = True

    return {
        'status': 'success',
        'is_exist_username': is_exist_username
    }


def get_master_password(user: User) -> str:
    """ Возвращает мастер пароль """
    try:
        master_password = MasterPassword.objects.get(user=user)
        return {
            'status': 'success',
            'result': master_password.password
        }
    except MasterPassword.DoesNotExist:
        return {
            'status': 'error',
            'result': 'doesnotexist'
        }


def check_if_password_correct(password1: str, password2: str) -> str:
    """ Проверка корректности пароля """
    if password1 != password2:
        return 'broken rule [pass == pass2]'
    if len(password1) < 8:
        return 'broken rule [len > 8]'
    if re.search('[a-z]', password1) is None:
        return 'broken rule [a-z]'
    if re.search('[A-Z]', password1) is None:
        return 'broken rule [A-Z]'
    if re.search('[0-9]', password1) is None:
        return 'broken rule [0-9]'

    return 'success'


def base_view(function):
    """ Декоратор для вьюшек, обрабатывает исключения """

    @functools.wraps(function)
    def wrapper(request, *args, **kwargs):
        try:
            with transaction.atomic():
                if not request.user.is_staff and SiteSetting.objects.get(name='site_in_service').value == 'true':
                    context = {
                        'title': 'Сайт закрыт на техническое обслуживание',
                        'static_version': STATIC_VERSION
                    }
                    return render(request, 'site_in_service.html', context)
                return function(request, *args, **kwargs)
        except Exception:
            if DEBUG:
                log.error(traceback.format_exc())
            write_error_to_log_file('ERROR', request.user, traceback.format_exc())
            return HttpResponseServerError(render(request, '500.html'))

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


def write_error_to_log_file(error_type: str, user: User, traceback_format_exc: str) -> None:
    """ Запись исключения в файл """
    try:
        _log_file = open(BASE_DIR + '/logs/log.json')
        log_file = _log_file.read()
        _log_file.close()
        text = json.loads(log_file)

        with open(BASE_DIR + '/logs/log.json', 'w+') as f:
            text.update({
                len(text): {
                    'type': error_type,
                    'user': str(user),
                    'date': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                    'traceback': traceback_format_exc
                }
            })
            f.write(
                json.dumps(text, indent=4)
            )

        # Если размер файла больше либо равен 10 мегабайт архивируем логи
        if len(log_file) >= 10485760:
            with zipfile.ZipFile(
                BASE_DIR +
                '/logs/log_json__' +
                datetime.now().strftime('%d-%m-%Y_%H-%M-%S') +
                '__.zip', 'w') as arzip:
                arzip.write(BASE_DIR + '/logs/log.json')
                log_file = open(BASE_DIR + '/logs/log.json', 'w+')
                log_file.write(json.dumps(json.loads('{}'), indent=4))
                log_file.close()
    except FileNotFoundError:
        if not os.path.exists(BASE_DIR + '/logs'):
            os.mkdir(BASE_DIR + '/logs')

        log_file = open(BASE_DIR + '/logs/log.json', 'w')
        text = json.loads('{}')
        text.update({
            len(text): {
                'type': error_type,
                'user': str(user),
                'date': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                'traceback': traceback_format_exc
            }
        })
        log_file.write(json.dumps(text, indent=4))
        log_file.close()
