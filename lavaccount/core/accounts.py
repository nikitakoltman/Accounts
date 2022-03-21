
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
