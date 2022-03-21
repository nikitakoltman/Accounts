
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

from django.db import transaction
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import render

from lavaccount.settings import (BASE_DIR, DEBUG,
                                 DONATION_NOTIFICATION_SECRET_KEY,
                                 IPINFO_IO_TOKEN, SITE_PROTOCOL,
                                 STATIC_VERSION, SUPPORT_EMAIL)
from loguru import logger as log

from .models import (Account, Donation, LoginHistory, MasterPassword,
                     SiteSetting)


def get_logs() -> list:
    """ Возвращает логи """
    logs = read_log_file(BASE_DIR + '/logs/log.json')
    if logs != '{}':
        return sorted_logs(logs)
    else:
        return json.loads(logs)


def read_log_file(path: str) -> json:
    """ Читает файл с логами и возвращает json """
    try:
        with open(path) as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return '{}'


def sorted_logs(logs: json) -> list:
    """ Сортировка логов по дате, чем раньше тем выше """
    return sorted(logs.items(), key=lambda kv: kv[1]['date'], reverse=True)


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
