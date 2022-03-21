import functools
import traceback

from django.db import transaction
from django.http import HttpResponseServerError
from django.shortcuts import render
from lavaccount.settings import DEBUG, STATIC_VERSION
from loguru import logger as log

import lav_logger

from .models import SiteSetting


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
            lav_logger.write_error_to_log_file(
                'ERROR', request.user, traceback.format_exc())
            return HttpResponseServerError(render(request, '500.html'))

    return wrapper
