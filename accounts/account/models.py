from django.db import models


class Account(models.Model):
    """ Аккаунты пользователя """

    site = models.CharField('Сайт', max_length=255)
    description = models.CharField('Описание', max_length=255)
    login = models.CharField('Логин', max_length=255)
    password = models.CharField('Пароль', max_length=255)
    user = models.CharField('Пользователь', max_length=255)
    updated = models.DateTimeField(
        'Обновлено', auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(
        'Создано', auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.id) + ' (' + self.user + ')'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ["-id", "-timestamp"]


class MasterPassword(models.Model):
    """ Мастер пароль пользователя """

    user = models.CharField('Пользователь', max_length=255)
    value = models.CharField('Значение', max_length=255)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Мастер пароль'
        verbose_name_plural = 'Мастер пароли'
