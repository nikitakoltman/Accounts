from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """ Аккаунты пользователя """
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    site = models.CharField('Сайт', max_length=255)
    description = models.CharField('Описание', max_length=255)
    login = models.CharField('Логин', max_length=255)
    password = models.CharField('Пароль', max_length=255)
    updated = models.DateTimeField(
        'Обновлено', auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(
        'Создано', auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{self.id} ({self.user.username})'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ["-id", "-timestamp"]


class MasterPassword(models.Model):
    """ Мастер пароль пользователя """
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    password = models.CharField('Пароль', max_length=255)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Мастер пароль'
        verbose_name_plural = 'Мастер пароли'


class TokenConfirmEmail(models.Model):
    """ Токен подтверждения электронной почты """
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    token = models.CharField("Токен", max_length=255)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'