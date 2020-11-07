# LavAccount
Проект для удобного хранения и управления своими аккаунтами сайтов.

## Install

Клонируйте данный репозиторий и перейдите в каталог "LavAccount".
```
git clone https://github.com/nikitakoltman/LavAccount
cd LavAccount
```
Создайте и активируйте виртуальное окружение python.
```
python3 -m venv env
source env/bin/activate
```
Установите зависимости.
```
pip install -r requirements.txt
```
Перейдите в директорию "LavAccount/lavaccount/lavaccount" и создайте файл ".env".
```
cd lavaccount/lavaccount
cp .env
```
Заполните в нем нужные параметры.
```
DJANGO_SECRET_KEY = 'secret'
DONATION_NOTIFICATION_SECRET_KEY = 'secret'

SUPPORT_EMAIL = 'support@domain.ru'

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.domain.ru'
EMAIL_HOST_USER = 'host@domain.ru'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587

YANDEX_MONEY_WALLET_NUMBER = 'number'
YANDEX_MONEY_DEFAULT_SUM = '100'
```
Вернитесь в директорию "LavAccount/lavaccount" и проведите миграции.
```
cd ..
python3 manage.py migrate
```
Создайте пользователя.
```
python3 manage.py createsuperuser
```
Активируйте сервер и пользуйтесь.
```
python3 manage.py runserver
```
