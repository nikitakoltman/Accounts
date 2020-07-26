from django.db import models


class Account(models.Model):
    """ Аккаунты пользователя """

    site = models.CharField('Сайт', max_length=255, default=None)
    description = models.CharField('Описание', max_length=255, default=None)
    login = models.CharField('Логин', max_length=255, default=None)
    password = models.CharField('Пароль', max_length=255, default=None)
    user_name = models.CharField('Имя пользователя', max_length=255, default=None)
    updated = models.DateTimeField(
        'Обновлено', auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(
        'Создано', auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.id) + ' (' + self.user_name + ')'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ["-id", "-timestamp"]


class MasterPassword(models.Model):
    """ Мастер пароль пользователя """

    user_name = models.CharField('Имя пользователя', max_length=255, default=None)
    value = models.CharField('Значение', max_length=255, default=None)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'Мастер пароль'
        verbose_name_plural = 'Мастер пароли'
