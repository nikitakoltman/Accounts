import datetime
import locale
import re
import json

from api import service
from api.models import Account, MasterPassword, LoginHistory
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from django.urls import reverse
from django.views.generic import TemplateView
from lavaccount.settings import static_version

from loguru import logger as log

from .forms import RegisterForm, MasterPasswordResetForm, EmailChangeForm, LoginForm

# Русская локализация для даты
locale.setlocale(locale.LC_ALL, "")


# TODO: Удалить
def email(request):
    context = {
        'username': request.user.username,
        'protocol': 'https',
        'domain': 'lavaccount.ru',
        'uid': 'MQ%5B0-9A-Za-z_%5',
        'token': '-z%5D%7B1,13%7D-%5B0-9A-Za-z%5D%',
        'email': service.hiding_email(request.user.email)
    }
    # registration_email_confirm_email
    # email_change_notification_to_old_email
    # email_change_email
    return render(request, 'email/registration_email_confirm_email.html', context)


@service.base_view
def index(request):
    """ Главная страница """
    context = {
        'static_version': static_version
    }
    #Account.objects.get(user='22222')

    if not request.user.is_authenticated:
        return render(request, 'landing.html', context)

    context.update({
        'accounts': Account.objects.filter(user=request.user),
        'master_password': service.get_master_password(user=request.user)
    })
    return render(request, 'home.html', context)


@service.base_view
def logs(request):
    """ Страница с отображением последних логов """
    if not request.user.is_superuser:
        return HttpResponseNotFound()

    file = open('logs/logs.log.json')
    logs = json.loads(file.read())
    logs = sorted(logs.items(), reverse=True)
    file.close()

    context = {
        'logs': logs,
        'static_version': static_version
    }
    return render(request, 'logs.html', context)


def noscript(request):
    """ Страница отображаемая если пользователь отключит javascript """
    context = {
        'static_version': static_version
    }
    return render(request, 'noscript.html', context)


@service.base_view
def lk(request):
    """ Личный кабинет пользователя """
    login_history = LoginHistory.objects.filter(user=request.user).order_by('-date')
    lh_date = dict()
    today = datetime.datetime.today()
    for lh in login_history:
        if lh.date.day == today.day:
            string = f'Сегодня в {lh.date.hour}:{lh.date.strftime("%M")}'
        elif lh.date.day == today.day - 1:
            string = f'Вчера в {lh.date.hour}:{lh.date.strftime("%M")}'
        elif lh.date.year == today.year:
            string = lh.date.strftime("%d %B") + f' в {lh.date.hour}:{lh.date.strftime("%M")}'
        else:
            string = lh.date.strftime("%d %B %Y") + f' в {lh.date.hour}:{lh.date.strftime("%M")}'
        lh_date.update({
            lh.id: string
        })

    context = {
        'title': 'Личный кабинет',
        'login_history': login_history,
        'lh_date': lh_date,
        'static_version': static_version
    }
    return render(request, 'lk.html', context)


@register.filter
def get_item_dict(dictionary, key):
    """ Фильтр для шаблона. Получить значение словаря по ключу """
    return dictionary.get(key)


@service.base_view
def email_change(request):
    """ Изменить адрес электронной почты """
    context = {
        'title': 'Изменить почтовый адрес',
        'form': EmailChangeForm,
        'static_version': static_version
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(id=request.user.id)
        current_site = Site.objects.get_current()
        service.confirm_email(
            user=user,
            email=email,
            subject='Привязка email к аккаунту',
            template='email_change_email'
        )
        service.send_email(
            email=user.email,
            subject='Привязка email к аккаунту',
            template='email_change_notification_to_old_email',
            context={
                'email': service.hiding_email(email),
                'username': user.username,
                'domain': current_site.domain
            }
        )
        user.email = email
        user.profile.is_active_email = False
        user.save()
        return redirect(reverse("email_change_done_url"))
    return render(request, 'email/email_change_form.html', context)


@service.base_view
def email_change_done(request):
    """ Страница которая говорит о том что письмо с
    инструкциями по изменению почтового адреса отправлено """
    context = {
        'title': 'Письмо с инструкциями по изменению почтового адреса отправлено',
        'static_version': static_version
    }
    return render(request, 'email/email_change_done.html', context)


@service.base_view
def email_change_complete(request):
    """ Страница которая говорит о том что
    изменение адреса почты завершено """
    context = {
        'title': 'Изменение адреса почты завершено',
        'static_version': static_version
    }
    return render(request, 'email/email_change_complete.html', context)


@service.base_view
def confirm_email_done(request):
    """ Страница которая говорит о том что
    отправленно письмо подтверждения почты после регистрации """
    context = {
        'title': 'Письмо отправленно',
        'static_version': static_version
    }
    return render(request, 'email/confirm_email_done.html', context)


@service.base_view
def confirm_email_complete(request):
    """ Страница которая говорит о том что
    пользователь успешно подтвердили почту после регистрации """
    valid = False

    if 'valid' in request.session:
        valid = request.session['valid']
        del request.session['valid']

    context = {
        'title': 'Подтверждение почты',
        'valid': valid,
        'static_version': static_version
    }
    return render(request, 'email/confirm_email_complete.html', context)


@service.base_view
def confirm_email(request):
    """ Отправка письма о подтверждении
    почты после регистрации """
    if not request.user.is_authenticated:
        return redirect(reverse("home_url"))
    service.confirm_email(
        user=request.user,
        email=request.user.email,
        subject='Добро пожаловать в LavAccount',
        template='registration_email_confirm_email'
    )
    return redirect(reverse("confirm_email_done_url"))


def activate_email(request, uidb64, token):
    """ Активация почты """
    if not request.user.is_authenticated:
        return redirect(reverse("lav_login"))

    if service.activate_email(uidb64, token):
        request.session['valid'] = True
    return redirect(reverse("confirm_email_complete_url"))


@service.base_view
def master_password_reset(request):
    """ Сброс мастер пароля """
    if not request.user.is_authenticated:
        return redirect(reverse("home_url"))

    context = {
        'title': 'Сброс мастер пароля',
        'form': MasterPasswordResetForm,
        'form_message': 'None',
        'static_version': static_version
    }

    try:
        is_master_password = False

        if MasterPassword.objects.filter(user=request.user).exists():
            is_master_password = True

        context.update({
            'master_password': is_master_password
        })

        if request.method == 'POST':
            password = request.POST.get('password')

            if service.master_password_reset(request.user, password):
                return redirect(reverse("home_url"))
            else:
                context.update({
                    'form_message': 'Password is not valid'
                })
    except Exception as err:
        context.update({
            'form_message': err
        })
    return render(request, 'registration/master_password_reset.html', context)


@service.base_view
def create_account(request):
    """ Создает аккаунт """
    # Если запрос был не ajax, а например по прямой ссылке...
    if not request.is_ajax():
        return HttpResponse(status=404)

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
    if not request.is_ajax():
        return HttpResponse(status=404)

    account_id = request.POST.get('account_id', None)
    answer = service.delete_account(account_id)
    return service.json_response(answer)


@service.base_view
def change_info_account(request):
    """ Изменяет информацию об аккаунте """
    if not request.is_ajax():
        return HttpResponse(status=404)

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
    if not request.is_ajax():
        return HttpResponse(status=404)

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


@service.base_view
def check_username(request):
    """ Проверяет существование имени в БД """
    if not request.is_ajax():
        return HttpResponse(status=404)

    username = request.POST.get('username', None)
    answer = service.check_username(username)
    return service.json_response(answer)


@service.base_view
def lav_login(request):
    """ Авторизация пользователей """
    if request.user.is_authenticated:
        return redirect(reverse("home_url"))

    context = {
        'form': LoginForm,
        'form_message': 'None',
        'static_version': static_version
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        system = request.POST.get('system')
        browser = request.POST.get('browser')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            service.new_login_history(
                request=request,
                system=system,
                browser=browser
            )
            return redirect(reverse("home_url"))
        else:
            context.update({
                'form_message': 'Login error'
            })
    return render(request, 'registration/login.html', context)


def check_if_password_correct(password1: str, password2: str) -> str:
    """ Проверка корректности пароля """
    if password1 != password2:
        return 'broken rule [pass == pass2]'
    if len(password1) < 8:
        return 'broken rule [len > 8]'
    elif re.search('[a-z]', password1) is None:
        return 'broken rule [a-z]'
    elif re.search('[A-Z]', password1) is None:
        return 'broken rule [A-Z]'
    elif re.search('[0-9]', password1) is None:
        return 'broken rule [0-9]'
    else:
        return 'success'


class RegisterView(TemplateView):
    """ Регистрация пользователей """
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("home_url"))

        context = {
            'form': RegisterForm,
            'form_message': 'None',
            'static_version': static_version
        }

        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            answer = check_if_password_correct(password1, password2)
            if answer == 'success':
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1
                    )

                    service.confirm_email(
                        user=user,
                        email=email,
                        subject='Добро пожаловать в LavAccount',
                        template='registration_email_confirm_email'
                    )

                    return redirect(reverse("lav_login"))
                except Exception as err:
                    context.update({
                        'form_message': err,
                        'username': username,
                        'email': email
                    })
            else:
                context.update({
                    'form_message': answer,
                    'username': username,
                    'email': email
                })
        return render(request, self.template_name, context)
